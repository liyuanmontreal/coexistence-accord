import matplotlib.pyplot as plt

def plot_dynamics(df):
    fig, ax = plt.subplots()
    for col in ["biodiv","economy","society","climate","trust"]:
        if col in df.columns:
            ax.plot(df["year"], df[col], label=col)
    ax.set_xlabel("Year")
    ax.set_ylabel("Index")
    ax.legend()
    return fig
