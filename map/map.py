import pandas as pd 
import matplotlib.pyplot as plot
import matplotlib.colors as mpcolors

#------------------------------------------------

def generate_map(input) -> None:
    # read file, no headers so assign column names
    file = pd.read_csv(input, header=None, names=['x','y','risk'])

    # csv -> grid
    heatmap_dat = file.pivot(index='y', columns='x', values='risk')

    # gradient for 0-> blue, 1-> red
    cmap = mcolors.LinearSegmentedColormap.from_list('blue_red', ['blue', 'red'])

    # make heatmap
    plt.figure(fisize=(8,8))
    plt.imshow(heatmap_dat, cmap=cmap, origin='lower', aspect='auto')
    plt.colorbar(label='Risk')
    plt.title('Risk Heat Map')
    plt.tight_layout

    plt.savefig(f'map_{input}.png')

#------------------------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python map.py <input.csv>")
    else:
        generate_map(sys.argv[1])