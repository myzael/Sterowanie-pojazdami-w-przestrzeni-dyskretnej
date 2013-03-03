import com.google.gson.*;

import java.awt.*;
import java.lang.reflect.Type;

public class StateDeserializer implements JsonDeserializer<State> {
    @Override
    public State deserialize(JsonElement jsonElement, Type type, JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {
        JsonArray jsonArray = jsonElement.getAsJsonArray();
        //   System.out.println(jsonArray);
        State state = new State();
        state.speed = jsonArray.get(2).getAsInt();
        state.position = new Point(jsonArray.get(0).getAsJsonArray().get(0).getAsInt(), jsonArray.get(0).getAsJsonArray().get(1).getAsInt());
        state.velocity = new Vector();
        state.velocity.x = jsonArray.get(1).getAsJsonArray().get(0).getAsInt();
        state.velocity.y = jsonArray.get(1).getAsJsonArray().get(1).getAsInt();
        return state;
    }
}