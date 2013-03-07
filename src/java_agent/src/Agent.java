import com.google.gson.*;
import org.eclipse.jetty.server.Request;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.AbstractHandler;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.awt.*;
import java.io.IOException;


public class Agent extends AbstractHandler {

    @Override
    public void handle(String s, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        String json = request.getReader().readLine();
        System.out.println(json);
        GsonBuilder builder = new GsonBuilder();
        builder.registerTypeAdapter(State.class, new StateDeserializer());
        builder.registerTypeAdapter(Vector.class, new VectorDeserializer());
        builder.registerTypeAdapter(Point.class, new PointDeserializer());
        Gson gson = builder.create();
        Query query = gson.fromJson(json, Query.class);

        response.setContentType("text/html;charset=utf-8");
        response.setStatus(HttpServletResponse.SC_OK);
        baseRequest.setHandled(true);
        Response r = getResponse(query);
        String move = r.toString();
        System.out.println(move);
        response.getWriter().print(move);
        response.getWriter().close();
    }

    private Response getResponse(Query query) {
        Response r = new Response();
        r.robotID = query.id;
        r.move = query.allowedMoves[0].position;
        r.speed = query.allowedMoves[0].speed;
        r.velocity = query.allowedMoves[0].velocity;
        return r;
    }

    public static void main(String[] args) throws Exception {
        Server server = new Server(Integer.parseInt(args[0]));
        server.setHandler(new Agent());
        server.start();
        server.join();
    }

}
