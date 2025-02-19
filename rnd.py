import torch
import numpy as np
from feedforward import Feedforward

class RND():
    def __init__(self, input_dim, output_dim, config):
        self.target = Feedforward(input_size = input_dim, hidden_size=config["hiddensize"], 
                                  output_size = output_dim, activation="tanh")
        self.predictor = Feedforward(input_size = input_dim, hidden_size=config["hiddensize"], 
                                  output_size = output_dim, activation="tanh")
        self.optimizer=torch.optim.Adam(self.predictor.parameters(), 
                                        lr=config["alpha"], 
                                        eps=0.000001)
        self.loss = torch.nn.MSELoss()

    def intrinsic_reward(self, observations):
        output_target = self.target(observations).detach()
        output_prediction = self.predictor(observations)
        reward = self.loss(output_target, output_prediction)
        return reward

    def update_pred(self, reward):
        reward.backward()
        self.optimizer.step()