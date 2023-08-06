from __future__ import unicode_literals, print_function, division

from lightwood.encoders.time_series.helpers.rnn_helpers import *
from lightwood.helpers.device import get_devices
from lightwood.encoders.encoder_base import BaseEncoder

import numpy as np
import torch
import torch.nn as nn
from torch import optim


class RnnEncoder(BaseEncoder):

    def __init__(self, encoded_vector_size=4, train_iters=100, stop_on_error=0.01, learning_rate=0.01,
                 is_target=False, ts_n_dims=1):
        super().__init__(is_target)
        self.device, _ = get_devices()
        self._stop_on_error = stop_on_error
        self._learning_rate = learning_rate
        self._encoded_vector_size = encoded_vector_size
        self._train_iters = train_iters  # training epochs
        self._pytorch_wrapper = torch.FloatTensor
        self._encoder = EncoderRNNNumerical(input_size=ts_n_dims, hidden_size=self._encoded_vector_size).to(self.device)
        self._decoder = DecoderRNNNumerical(output_size=ts_n_dims, hidden_size=self._encoded_vector_size).to(self.device)
        self._parameters = list(self._encoder.parameters()) + list(self._decoder.parameters())
        self._optimizer = optim.AdamW(self._parameters, lr=self._learning_rate, weight_decay=1e-4)
        self._criterion = nn.MSELoss()
        self._prepared = False
        self._n_dims = ts_n_dims  # expected dimensionality of time series
        self._max_ts_length = 0
        self._sos = 0.0  # start of sequence for decoding
        self._eos = 0.0  # end of input sequence -- padding value for batches
        self._normalizer = MinMaxNormalizer()

    def to(self, device, available_devices):
        self.device = device
        self._encoder = self._encoder.to(self.device)
        return self

    def prepare_encoder(self, priming_data, feedback_hoop_function=None, batch_size=256):
        """
        The usual, run this on the initial training data for the encoder
        :param priming_data: a list of (self._n_dims)-dimensional time series [[dim1_data], ...]
        :param feedback_hoop_function: [if you want to get feedback on the training process]
        :param batch_size
        :return:
        """
        if self._prepared:
            raise Exception('You can only call "prepare_encoder" once for a given encoder.')

        # Convert to array and determine max length:
        for i in range(len(priming_data)):
            if not isinstance(priming_data[i][0], list):
                priming_data[i] = [priming_data[i]]
            self._max_ts_length = max(len(priming_data[i][0]), self._max_ts_length)

        if self._normalizer:
            self._normalizer.fit(priming_data)

        # decrease for small datasets
        if batch_size >= len(priming_data):
            batch_size = len(priming_data) // 2

        self._encoder.train()
        for i in range(self._train_iters):
            average_loss = 0
            data_idx = 0

            while data_idx < len(priming_data):

                # batch building
                data_points = priming_data[data_idx:min(data_idx + batch_size, len(priming_data))]
                batch = []
                for dp in data_points:
                    data_tensor = tensor_from_series(dp, self.device, self._n_dims,
                                                     self._eos, self._max_ts_length,
                                                     self._normalizer)
                    batch.append(data_tensor)

                # shape: (batch_size, timesteps, n_dims)
                batch = torch.cat(batch, dim=0).to(self.device)
                data_idx += batch_size

                # setup loss and optimizer
                steps = batch.shape[1]
                loss = 0
                self._optimizer.zero_grad()

                # encode
                encoder_hidden = self._encoder.initHidden(self.device)
                next_tensor = data_tensor[:, 0, :].unsqueeze(dim=1)  # initial input

                for tensor_i in range(steps - 1):
                    rand = np.random.randint(2)
                    # teach from forward as well as from known tensor alternatively
                    if rand == 1:
                        next_tensor, encoder_hidden = self._encoder.forward(
                            data_tensor[:, tensor_i, :].unsqueeze(dim=1),
                            encoder_hidden)
                    else:
                        next_tensor, encoder_hidden = self._encoder.forward(next_tensor.detach(), encoder_hidden)

                    loss += self._criterion(next_tensor, data_tensor[:, tensor_i + 1, :].unsqueeze(dim=1))

                # decode
                decoder_hidden = encoder_hidden
                next_tensor = torch.full((batch.shape[0], 1, batch.shape[2]), self._sos,
                                         dtype=torch.float32).to(self.device)
                tensor_target = torch.cat([next_tensor, batch], dim=1)  # add SOS token at t=0 to true input

                for tensor_i in range(steps - 1):
                    rand = np.random.randint(2)
                    # teach from forward as well as from known tensor alternatively
                    if rand == 1:
                        next_tensor, decoder_hidden = self._decoder.forward(
                            tensor_target[:, tensor_i, :].unsqueeze(dim=1),
                            decoder_hidden)
                    else:
                        next_tensor, decoder_hidden = self._decoder.forward(next_tensor.detach(), decoder_hidden)

                    loss += self._criterion(next_tensor, tensor_target[:, tensor_i + 1, :].unsqueeze(dim=1))

                average_loss += loss.item()
                loss.backward()
                self._optimizer.step()

            average_loss = average_loss / len(priming_data)

            if average_loss < self._stop_on_error:
                break
            if feedback_hoop_function is not None:
                feedback_hoop_function("epoch [{epoch_n}/{total}] average_loss = {average_loss}".format(
                    epoch_n=i + 1,
                    total=self._train_iters,
                    average_loss=average_loss))

        self._prepared = True

    def _encode_one(self, data, initial_hidden=None, return_next_value=False):
        """
        This method encodes one single row of serial data
        :param data: multidimensional time series as list of lists [[dim1_data], [dim2_data], ...]
                     (dim_data: string with format "x11, x12, ... x1n")
        :param initial_hidden: if you want to encode from an initial hidden state other than 0s
        :param return_next_value:  if you want to return the next value in the time series too

        :return:  either encoded_value or (encoded_value, next_value)
        """
        self._encoder.eval()
        with torch.no_grad():
            # n_timesteps inferred from query
            data_tensor = tensor_from_series(data, self.device, self._n_dims,
                                             self._eos, normalizer=self._normalizer)
            steps = data_tensor.shape[1]
            encoder_hidden = self._encoder.initHidden(self.device)
            encoder_hidden = encoder_hidden if initial_hidden is None else initial_hidden

            next_tensor = None
            for tensor_i in range(steps):
                next_tensor, encoder_hidden = self._encoder.forward(data_tensor[:, tensor_i, :].unsqueeze(dim=0),
                                                                    encoder_hidden)

        if return_next_value:
            return encoder_hidden, next_tensor
        else:
            return encoder_hidden

    def encode(self, column_data, get_next_count=None):
        """
        Encode a list of time series data
        :param column_data: a list of (self._n_dims)-dimensional time series [[dim1_data], ...] to encode
        :param get_next_count: default None, but you can pass a number X and it will return the X following predictions
                               on the series for each ts_data_point in column_data
        :return: a list of encoded time series or if get_next_count !=0 two lists (encoded_values, projected_numbers)
        """

        if not self._prepared:
            raise Exception('You need to call "prepare_encoder" before calling "encode" or "decode".')

        for i in range(len(column_data)):
            if not isinstance(column_data[i][0], list):
                column_data[i] = [column_data[i]]

        ret = []
        next = []

        for val in column_data:
            if get_next_count is None:
                encoded = self._encode_one(val)
            else:
                if get_next_count <= 0:
                    raise Exception('get_next_count must be greater than 0')

                hidden = None
                vector = val
                next_i = []

                for j in range(get_next_count):
                    hidden, next_reading = self._encode_one(vector, initial_hidden=hidden, return_next_value=True)
                    vector = [next_reading]
                    if j == 0:
                        encoded = hidden
                    next_i.append(next_reading)

                next_value = next_i[0][0].cpu()

                if self._normalizer:
                    next_value = torch.Tensor(self._normalizer.inverse_transform(next_value))

                next.append(next_value)

            ret.append(encoded[0][0].cpu())

        if get_next_count is None:
            return self._pytorch_wrapper(torch.stack(ret))
        else:
            return self._pytorch_wrapper(torch.stack(ret)), self._pytorch_wrapper(torch.stack(next))

    def _decode_one(self, hidden, steps):
        """
        Decodes a single time series from its encoded representation.
        :param hidden: time series embedded representation tensor, with size self._encoded_vector_size
        :param steps: as in decode(), defines how many values to output when reconstructing
        :return: decoded time series list
        """
        self._decoder.eval()
        with torch.no_grad():
            ret = []
            next_tensor = torch.full((1, 1, self._n_dims), self._sos, dtype=torch.float32).to(self.device)
            timesteps = steps if steps else self._max_ts_length
            for _ in range(timesteps):
                next_tensor, hidden = self._decoder.forward(next_tensor, hidden)
                ret.append(next_tensor)
            return torch.stack(ret)

    def decode(self, encoded_data, steps=None):
        """
        Decode a list of embedded multidimensional time series
        :param encoded_data: a list of embeddings [ e1, e2, ...] to be decoded into time series
        :param steps: fixed number of timesteps to reconstruct from each embedding.
        If None, encoder will output the largest length encountered during training.
        :return: a list of reconstructed time series
        """
        if not self._prepared:
            raise Exception('You need to call "prepare_encoder" before calling "encode" or "decode".')

        ret = []
        for _, val in enumerate(encoded_data):
            hidden = torch.unsqueeze(torch.unsqueeze(val, dim=0), dim=0).to(self.device)
            reconstruction = self._decode_one(hidden, steps).cpu().squeeze().T.numpy()

            if self._n_dims == 1:
                reconstruction = reconstruction.reshape(1, -1)

            if self._normalizer:
                reconstruction = self._normalizer.inverse_transform(reconstruction)

            ret.append(reconstruction)

        return self._pytorch_wrapper(ret)
