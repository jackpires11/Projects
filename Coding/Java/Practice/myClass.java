public class myClass {

    // The name of the class.
    String name;

    // The constructor for setting the name of the class.
    public myClass(String name) {
        this.name = name;
    }

    // Prints the name of the class!
    public void print() {
        System.out.println(name);
    }

    // The function called when the program is run.
    public static void main(String[] args) {
        myClass newClass = new myClass("Hooray!");
        newClass.print();
    }
}