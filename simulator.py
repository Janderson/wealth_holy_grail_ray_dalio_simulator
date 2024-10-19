import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import click

AUTHOR = "Janderson FFerreira (JJ)"


def corr2cov(p: np.ndarray, s: np.ndarray) -> np.ndarray:
    """
        Covariance matrix from corretion & Std Deviation
    """
    d = np.diag(s)
    return d @ p @ d


def plotter(dataframe, risk=0.1, params_num_asset=21, show_chart=True):
    plt.figure(figsize=(15, 5))
    plt.plot(dataframe)
    plt.title("The Holy Grail of Ray Dalio")
    plt.legend(dataframe.columns)
    plt.xlabel("# of Assets/Alphas in Portfolio")
    plt.ylabel("Annual Portfolio Std.Deviation")
    plt.xticks(list(range(0, params_num_asset-1)))
    #plt.yticks(np.arange(risk, 0, -0.1))
    print(f"showchart: {show_chart}")
    if show_chart:
        plt.show()
    else:
        plt.savefig("simulator-holy-grail-result.png")

def build_fraction_list(correlations):
    divisor = 100
    return [(corr/divisor) for corr in correlations]


def transform_input_correlations(correlations_str):
    return [int(item) for item in correlations_str.split(",")]


def simulator(correlations, param_return=.10, params_num_asset=20):
    param_means = param_stddev = param_return
    df = pd.DataFrame()
    results = []
    for correlation in build_fraction_list(correlations):
        result_list = []
        for num_assets in range(1, params_num_asset+1):
            corr_matrix = np.zeros((num_assets, num_assets), float)
            corr_matrix.fill(correlation)
            np.fill_diagonal(corr_matrix, 1)

            stddev = np.empty(num_assets, dtype='float')
            stddev.fill(param_stddev)
            mean = np.empty(num_assets, dtype='float')
            mean.fill(param_means)

            cov = corr2cov(corr_matrix, stddev)

            data = np.random.multivariate_normal(
                mean=mean,
                cov=cov,
                size=500
            )

            portfolio_returns = np.mean(data, axis=1)
            portfolio_risk = np.std(portfolio_returns)

            result_list.append(portfolio_risk)
            result = {
                "assets": num_assets,
                "correlation": correlation,
                "risk": portfolio_risk
            }
            results.append(result)

        df.insert(0, 'correlation: ' + str(correlation), result_list, True)
    return df


@click.command("simulator")
@click.option("--savefigure", default=False)
@click.option("--correlations", default="60,40,20,10,5")
@click.option("--expected_return", "expected_return", default=10, type=click.FLOAT)
@click.option("--num_assets", "num_assets", default=20)
def cmd_simulator(savefigure, correlations, expected_return, num_assets):
    print(f"Simulator of Ray Dalio 'Holy Grail' built by: {AUTHOR}")
    result_df = simulator(transform_input_correlations(correlations),
                          param_return=float(expected_return)/100,
                          params_num_asset=num_assets)
    #print(result_df.tail())
    plotter(result_df, show_chart=(not savefigure), params_num_asset=num_assets)


if __name__ == "__main__":
    cmd_simulator()
