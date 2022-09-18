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


def plotter(dataframe, show_chart=True):
    plt.figure(figsize=(12, 5))
    plt.plot(dataframe)
    plt.title("The Holy Grail of Ray Dalio")
    plt.legend(dataframe.columns)
    plt.xlabel("# of Assets/Alphas in Portfolio")
    plt.ylabel("Annual Portfolio Std.Deviation")
    if show_chart:
        plt.show()
    else:
        plt.savefig("simulator-holy-grail-result.png")


def simulator():
    print(f"Simulator of Ray Dalio 'Holy Grail' built by: {AUTHOR}")
    df = pd.DataFrame()
    mean_assets = .1
    stddev_assets = .1

    correlation_test_list = [
        .60, .40, .20, .10, 0
    ]
    for correlation in correlation_test_list:
        result_list = []
        for num_assets in range(1, 21):
            corr_matrix = np.zeros((num_assets, num_assets), float)
            corr_matrix.fill(correlation)
            np.fill_diagonal(corr_matrix, 1)

            stddev = np.empty(num_assets, dtype='float')
            stddev.fill(stddev_assets)
            mean = np.empty(num_assets, dtype='float')
            mean.fill(mean_assets)

            cov = corr2cov(corr_matrix, stddev)

            data = np.random.multivariate_normal(
                mean=mean,
                cov=cov,
                size=500
            )

            portfolio_returns = np.mean(data, axis=1)
            portfolio_risk = np.std(portfolio_returns)

            result_list.append(portfolio_risk)
            print(f"c: {correlation}"
                  f"assets: {num_assets}"
                  f"risk: {portfolio_risk:.5f}")

        df.insert(0, 'correlation: ' + str(correlation), result_list, True)
    return df


@click.command("simulator")
@click.option("--savefigure", default=False)
def cmd_simulator(savefigure):
    result_df = simulator()
    print(result_df.tail())
    plotter(result_df, show_chart=savefigure)


if __name__ == "__main__":
    cmd_simulator()
