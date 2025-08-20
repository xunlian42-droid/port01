class top {
    int x = 1;
    int y = 2;
}
class Middle extends Top {
    double x = 3.5;
    public void update() {
        super.update();
        y = 50;
    }
}
class Main {
    public static void main(String[] args) {
        Middle obj = new Bottom();
        obj.update();
        System.out.println(obj.x + ":" + obj.y);
    }
}