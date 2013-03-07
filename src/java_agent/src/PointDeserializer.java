import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;

import java.awt.*;
import java.lang.reflect.Type;

public class PointDeserializer implements JsonDeserializer<Point> {

    @Override
    public Point deserialize(JsonElement jsonElement, Type type, JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {
        return new Point(jsonElement.getAsJsonArray().get(0).getAsInt(), jsonElement.getAsJsonArray().get(1).getAsInt());
    }
}
