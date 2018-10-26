
// Create a map object

// Selecting the "Search" button
var search_btn = d3.select("#search-btn");
var tweetsTable = d3.select("tbody");

// logic to handle onClick event on "Search" button
search_btn.on("click", function() {

  console.log("Onclick Event on Search Button: Begin");
  //preventing refresh
  d3.event.preventDefault();

  var searchElement = "";
  var searchKeyword = "";

  searchElement = d3.select("#keyword");
  searchKeyword = searchElement.property("value").trim();
  if (searchKeyword != ""){
    console.log(`Search keyword is ${searchKeyword}`);
    tweetsTable.selectAll("tr").remove();
    // searchRadioElement = d3.select("input[name='sortby']");
    // sortby = searchRadioElement.property("value").trim();

    // sortby = $('input[name="sortby"]:checked').val()
    // console.log(`Sort Value is ${sortby}`);
    getCoffeeTweets(searchKeyword);
  }
  else
    alert("Please enter keyword to search tweets for!");

  //Calling the getYelpReview method to fetch Yelp Reviews
  
  console.log("Onclick Event on Search Button: End");
});

/*
@author - Saifee Dalal
@Name - getCoffeeTweets
@Input - keyword
@Output - JSON Response from Twitter
@Description - This function will call the flask route to tap Twitter API and fetch the response
*/
function getCoffeeTweets(searchKeyword){

  console.log("Inside getCoffeeTweets(): Begin");
  
  var url = "/getCoffeeTweets/"+searchKeyword;
  console.log("URL", url);
  d3.json(url,function(data) {
    console.log("Returned Response", data);
    
    console.log("tweets returned: ", data.statuses.length);
    if (data.statuses.length > 0){
      
      //document.getElementById("tablehead").classList.remove('invisible');
      d3.select("#tablehead")
        .classed("invisible", false);

      for (var i = 0; i < data.statuses.length; i++) {
        
        text = data.statuses[i].full_text;
        console.log("Text:", text);
        user = data.statuses[i].user.screen_name
        console.log("User:", user);
        created = data.statuses[i].created_at
        console.log("Created:", created);

        var mentions = "";

        if (data.statuses[i].entities.user_mentions.length > 0){
          // for (var j = 0; j < data.statuses[i].entities.user_mentions.length; j++){
          // for (var j = 0; j < 2; j++){
            mentions += "@";
            mentions += data.statuses[i].entities.user_mentions[0].screen_name
          //   mentions += ","
          // }
       }

        // if (mentions != null)
        //   mentions = mentions.substring(0,mentions.length-1);

        var row;
        var cell;
        row = tweetsTable.append("tr");
        cell = row.append("td");
        cell.text(user);
        cell = row.append("td");
        cell.text(mentions);
        cell = row.append("td");
        cell.text(text);
        cell = row.append("td");
        cell.text(created);
        

      }
    }

    else
      alert("No tweets found for the selected keyword!");

  });


};
