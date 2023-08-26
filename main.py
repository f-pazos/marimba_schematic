import compute_dimensions
import visualizer
import key_data
import calculator

def main(): 
    print(calculator.convert_to_imperial(0.837573))
    exit()
    naturals = key_data.read_keys("jeezus_naturals.csv")
    # compute_dimensions.compute_dimensions(naturals, 68.75, 1.875, 1.75)

    visualizer.visualize()


main()