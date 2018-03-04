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
                return L.marker(latlng, {
                    icon: L.icon({ iconUrl:'{{ marker.default_icon.url }}'}),
                });
                break;
        {% endfor %}
    }
};

function onEachFeature(feature, layer) {
    layer.bindPopup("Loading...");
    layer.on('click', function(e) {
        var popup = e.target.getPopup();
        var url=feature.properties.popup_url;
        $.get(url).done(function(data) {
            popup.setContent(data);
            popup.update();
        });
    });
}

geojsonOptions = {
    style: getStyle,
    pointToLayer: getPointToLayer,
    onEachFeature: onEachFeature,
};

{% for layer in layers %}
$.getJSON("/webmap/geojson/{{ layer.slug }}", function(geojson_layer){
    L.geoJSON(geojson_layer, geojsonOptions).addTo(window.map);
});
{% endfor %}
