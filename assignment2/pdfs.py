import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.integrate import quad
from loguru import logger  

class ProbabilityDensityFunction:
    def __init__(self, x, y, spline_order=3, normalize=True):
        """
        Initializes the ProbabilityDensityFunction with a spline-based interpolation.

        Parameters:
        x (np.ndarray): array of x-values (grid points) for the PDF.
        y (np.ndarray): array of y-values (PDF values at the grid points).
        spline_order (int): order of the spline interpolation (default is cubic spline, 3).
        normalize (bool): whether to normalize `y` so that it integrates to 1 (default: True).
        """
        # Ensure x and y are valid
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")
        if len(x) < 2:
            raise ValueError("x and y must contain at least two elements each.")
        
        # Store x and y
        self.x = x
        self.y = y

        # Normalize y to make it a valid PDF if requested
        if normalize:
            total_area, _ = quad(InterpolatedUnivariateSpline(x, y), x[0], x[-1])
            self.y_normalized = y / total_area
        else:
            self.y_normalized = y

        # Create the spline
        self.spline = InterpolatedUnivariateSpline(x, self.y_normalized, k=spline_order)

    def evaluate(self, points):
        """
        Evaluates the PDF at specified points.

        Parameters:
        points (float or np.ndarray): A single value or an array of values to evaluate the PDF at.

        Returns:
        np.ndarray: The PDF values at the specified points.
        """
        return self.spline(points)

    def probability_in_interval(self, a, b):
        """
        Calculates the probability that a random variable falls within the interval [a, b].

        Parameters:
        a (float): Start of the interval.
        b (float): End of the interval.

        Returns:
        float: Probability in the interval [a, b].
        """
        # Ensure the bounds are within the x range
        if a < self.x[0] or b > self.x[-1]:
            raise ValueError("Interval bounds must be within the range of x values.")
        
        # Integrate PDF over the interval
        probability, _ = quad(self.spline, a, b)
        return probability

    def sample(self, num_samples=1):
        """
        Generates random samples according to the PDF.

        Parameters:
        num_samples (int): Number of random samples to generate (default: 1).

        Returns:
        np.ndarray: Array of random samples following the distribution of the PDF.
        """
        # Generate uniform random numbers
        uniform_samples = np.random.rand(num_samples)
        
        # Compute CDF by integrating PDF over x values
        cdf_x = np.linspace(self.x[0], self.x[-1], len(self.x))
        cdf_y = np.array([quad(self.spline, self.x[0], xi)[0] for xi in cdf_x])

        # Normalize CDF to range from 0 to 1
        cdf_y /= cdf_y[-1]
        
        # Create an inverse CDF interpolation for sampling
        inverse_cdf = InterpolatedUnivariateSpline(cdf_y, cdf_x, k=1)
        
        # Use inverse CDF to transform uniform samples to follow the PDF
        return inverse_cdf(uniform_samples)


if __name__ == '__main__':
    logger.info("Starting the Probability Density Function Interactive Draft")

    # Create a sample distribution
    x = np.linspace(0, 10, 100)
    y = np.exp(-(x - 5)**2 / 2)  # Gaussian-like distribution
    
    pdf = ProbabilityDensityFunction(x, y)
    logger.success("Created a Gaussian-like Probability Density Function")

    while True:
        print("\nWhat would you like to do?")
        print("1. Evaluate PDF at a point")
        print("2. Calculate probability in an interval")
        print("3. Generate random samples")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            point = float(input("Enter a point to evaluate the PDF: "))
            result = pdf.evaluate(point)
            logger.info(f"PDF value at x={point}: {result}")

        elif choice == '2':
            a = float(input("Enter the start of the interval: "))
            b = float(input("Enter the end of the interval: "))
            try:
                result = pdf.probability_in_interval(a, b)
                logger.info(f"Probability between {a} and {b}: {result}")
            except ValueError as e:
                logger.error(f"Error: {e}")

        elif choice == '3':
            num_samples = int(input("Enter the number of samples to generate: "))
            samples = pdf.sample(num_samples)
            logger.success(f"Generated {num_samples} samples")
            logger.info(f"Sample mean: {np.mean(samples)}")
            logger.info(f"Sample standard deviation: {np.std(samples)}")

        elif choice == '4':
            logger.info("Exiting the program")
            break

        else:
            logger.warning("Invalid choice. Please enter a number between 1 and 4.")

    logger.info("Thank you for using the Probability Density Function Draft!")