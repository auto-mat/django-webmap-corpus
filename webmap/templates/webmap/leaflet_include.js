geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

function getStyle(feature){
    switch (feature.properties.marker) {
        {% for marker in markers %}
            case {{ marker.id }}:
                return {
                    color: '{{ marker.line_color }}',
                    weight: {{ marker.line_width|floatformat:"0" }},
                };
                break;
        {% endfor %}
    }
};

function getPointToLayer(feature, latlng){
    switch (feature.properties.marker){
        {% for marker in markers %}
            case {{ marker.id }}:
                return L.marker(latlng, {icon: L.icon({ iconUrl:'{{ marker.default_icon.url }}'})});
                break;
        {% endfor %}
    }
};

function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.desc) {
        description = "<h4>" + feature.properties.name + "</h4>" + feature.properties.desc + "<br/><small>" + feature.properties.desc_extra + "</small>";
        return layer.bindPopup(description);
    }
}

geojsonOptions = {
    style: getStyle,
    pointToLayer: getPointToLayer,
    onEachFeature: onEachFeature,
};

$.getJSON("/webmap/geojson", function(geojson_layer){
    L.geoJSON(geojson_layer, geojsonOptions).addTo(window.map);
});
