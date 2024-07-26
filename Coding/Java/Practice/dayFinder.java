
//Used for a date class.
import java.time.LocalDate;
//Used to read user input.
import java.util.Scanner;

public class dayFinder {

    // The date you're trying to determine the day of.
    LocalDate date;

    public dayFinder(int year, int month, int day) {
        this.date = LocalDate.of(year, month, day);
    }

    public int[] obtainingDate() {
        Scanner userData = new Scanner(System.in);
        System.out.println("Please enter the year for which you wish to know the day of:");
        int year = Integer.parseInt(userData.nextLine());
        System.out.println("Please enter the month for which you wish to know the day of:");
        int month = Integer.parseInt(userData.nextLine());
        System.out.println("Please enter the day for which you wish to know the day of:");
        int day = Integer.parseInt(userData.nextLine());
        // Adds the obtained dates to an array and returns them for processing.
        int arr[] = { year, month, day };
        userData.close();
        return (arr);
    }

    // The initial running code.
    public static void main(String[] args) {

    }

}