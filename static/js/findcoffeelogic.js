
// Create a map object

   var myMap = L.map("map", {
    center: [35, -100],
    zoom: 4
  });


  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets-basic",
    accessToken: API_KEY
  }).addTo(myMap);

  var markerGroup = L.layerGroup().addTo(myMap);

  function setMapLocation(lat,long,zoom){
    // myMap.removeLayer();
    myMap.setView(new L.LatLng(lat, long), zoom);
    markerGroup.clearLayers();
  }


// Selecting the "Search" button
var search_btn = d3.select("#search-btn");

// logic to handle onClick event on "Search" button
search_btn.on("click", function() {

  console.log("Onclick Event on Search Button: Begin");
  //preventing refresh
  d3.event.preventDefault();

  var searchElement = "";
  var searchRadioElement = "";
  var searchLocation = "";
  var sortby = "";

  searchElement = d3.select("#location");
  searchLocation = searchElement.property("value").trim();
  if (searchLocation != ""){
    console.log(`Search location is ${searchLocation}`);
    // searchRadioElement = d3.select("input[name='sortby']");
    // sortby = searchRadioElement.property("value").trim();

    sortby = $('input[name="sortby"]:checked').val()
    console.log(`Sort Value is ${sortby}`);
    getYelpReview(searchLocation, sortby);
  }
  else
    alert("Please enter location!");

  //Calling the getYelpReview method to fetch Yelp Reviews
  
  console.log("Onclick Event on Search Button: End");
});

/*
@author - Saifee Dalal
@Name - getYelpReview
@Input - inputData
@Output - JSON Response from Yelp
@Description - This function will call the flask route to tap YELP API and fetch the response
*/
function getYelpReview(searchLocation, sortby){

  console.log("Inside getYelpReview(): Begin");
  
  var url = "/getYelpReview/"+searchLocation+"/"+sortby;
  console.log("URL", url);
  d3.json(url,function(data) {
    console.log("Returned Response", data);
    
    if (data.businesses != null){
      
      var latlong = data.businesses[0].coordinates;
      console.log("LatLong:", latlong);
      var latitude = data.businesses[0].coordinates.latitude
      console.log("Latitude:", latitude);
      var longitude = data.businesses[0].coordinates.longitude
      console.log("Longitude:", longitude);

      
      setMapLocation(latitude,longitude,11);

      for (var i = 0; i < data.businesses.length; i++) {
        
        latlong = data.businesses[i].coordinates;
        console.log("LatLong:", latlong);
        latitude = data.businesses[i].coordinates.latitude
        console.log("Latitude:", latitude);
        longitude = data.businesses[i].coordinates.longitude
        console.log("Longitude:", longitude);

        L.marker([latitude,longitude])
          .bindPopup("<div class= content><a target = _blank href = "+data.businesses[i].url+"><h5><b>"+ data.businesses[i].name+ "</b></h5></a> <img src = " +data.businesses[i].image_url+"> <h6> <b>Address: </b>" + data.businesses[i].location.display_address + " <hr> <b> Review Count:</b>" + data.businesses[i].review_count + "<br><b>Rating:</b>" + data.businesses[i].rating + "<br><b>Price:</b>" + data.businesses[i].price + "</h6></div>")
          .addTo(markerGroup);
      }
    }

    else
      alert("No result found for the selected location!");

  });


};
