import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;

import java.lang.reflect.Type;

public class VectorDeserializer implements JsonDeserializer<Vector> {

    @Override
    public Vector deserialize(JsonElement jsonElement, Type type, JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {
        Vector vector = new Vector();
        vector.x = jsonElement.getAsJsonArray().get(0).getAsInt();
        vector.y = jsonElement.getAsJsonArray().get(1).getAsInt();
        return vector;
    }
}
