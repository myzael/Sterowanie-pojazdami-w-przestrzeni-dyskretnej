import java.awt.*;

public class Response {
    public String robotID;
    public Point move;
    public int speed;
    public Vector velocity;

    @Override
    public String toString() {
        return "{\"robotID\" : " + robotID + ", \"move\": [ " + move.x + ", " + move.y + " ], \"speed\" : " + speed + ", \"velocity\" : [" + velocity.x + ", " + velocity.y + "] }";
    }
}
