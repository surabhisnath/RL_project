import torch
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Feedforward_RND(torch.nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes=[100,100]):
        super(Feedforward_RND, self).__init__()
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        layer_sizes = [self.input_size] + self.hidden_sizes
        self.layers = torch.nn.ModuleList(
            [torch.nn.Linear(i, o) for i, o in zip(layer_sizes[:-1], layer_sizes[1:])]
        ).to(device)
        self.activations = [torch.nn.Tanh() for l in self.layers]
        self.readout = torch.nn.Linear(self.hidden_sizes[-1], self.output_size).to(device)

    def forward(self, x):
        x = x.to(device)
        for layer, activation_fun in zip(self.layers, self.activations):
            x = activation_fun(layer(x))
        return self.readout(x)

    def predict(self, x):
        with torch.no_grad():
            return self.forward(torch.from_numpy(x.astype(np.float32))).numpy()

activation_mapping = {
    "relu": "ReLU",
    "sigmoid": "Sigmoid",
    "tanh": "Tanh"
}

class Feedforward(torch.nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int, activation: str):
        """Initialization."""
        super(Feedforward, self).__init__()

        try:
            actfn = activation_mapping[activation.lower()]
        except KeyError:
            raise ValueError("Activation function can only be 'relu', 'sigmoid', or 'tanh'")

        activation_fn = getattr(torch.nn, actfn)

        self.layers = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            activation_fn(),
            torch.nn.Linear(hidden_size, hidden_size),
            activation_fn(),
            torch.nn.Linear(hidden_size, output_size),
        ).to(device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x.to(device))

    def predict(self, x):
        with torch.no_grad():
            return self.forward(torch.from_numpy(x.astype(np.float32))).cpu().numpy()


class Feedforward_Dueling(torch.nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int, activation: str):
        """Initialization."""
        super(Feedforward_Dueling, self).__init__()

        try:
            actfn = activation_mapping[activation.lower()]
        except KeyError:
            raise ValueError("Activation function can only be 'relu', 'sigmoid', or 'tanh'")

        # activation_fn = getattr(torch.nn, actfn)
        activation_fn = torch.nn.ReLU

        self.feature_layer = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            activation_fn(),
        ).to(device)

        self.advantage_layer = torch.nn.Sequential(
            torch.nn.Linear(hidden_size, hidden_size),
            activation_fn(),
            torch.nn.Linear(hidden_size, output_size),
        ).to(device)

        self.value_layer = torch.nn.Sequential(
            torch.nn.Linear(hidden_size, hidden_size),
            activation_fn(),
            torch.nn.Linear(hidden_size, 1),
        ).to(device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.to(device)
        feature = self.feature_layer(x)
        value = self.value_layer(feature)
        advantage = self.advantage_layer(feature)
        return value + advantage - advantage.mean(dim=-1, keepdim=True)

    def predict(self, x):
        with torch.no_grad():
            return self.forward(torch.from_numpy(x.astype(np.float32))).cpu().numpy()
