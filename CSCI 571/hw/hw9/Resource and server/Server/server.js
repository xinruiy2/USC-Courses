const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const querystring = require('query-string');
const axios = require('axios');

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE');
    if('OPTIONS' === req.method) {
        res.sendStatus(200);
    } else {
        console.log(`${req.ip} ${req.method} ${req.url}`);
        next();
    }
})

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', async function(req,res) {
    
  if(req.query.productID){
      var url = "http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid=XinruiYi-571proje-PRD-22eae7200-0aaa1f3f&siteid=0&version=967&ItemID=" 
      + req.query.productID + "&IncludeSelector=Description,Details,ItemSpecifics";
  }else{
      var x = 0;
      var url = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=MuzhenLi-webtechn-PRD-d2eb49443-5d70afd1&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=';
      console.log(req.query.maxPrice)
      url = url + req.query.keyword + '&paginationInput.entriesPerPage=50&sortOrder=' + req.query.sortOrder;
      if(req.query.maxPrice != "null"){
        url = url + "&itemFilter("+x.toString()+").name=MaxPrice&itemFilter(" + x.toString() + ").value=" + req.query.maxPrice + "&itemFilter(" + x.toString() + ").paramName=Currency&itemFilter(" + x.toString() + ").paramValue=USD";
        x += 1;
      }
      if(req.query.minPrice != "null"){
        url = url + "&itemFilter("+x.toString()+").name=MinPrice&itemFilter(" + x.toString() + ").value=" + req.query.minPrice + "&itemFilter(" + x.toString() + ").paramName=Currency&itemFilter(" + x.toString() + ").paramValue=USD";
        x += 1;
      }
//      if(req.query.ret != 'false'){
//        url = url + "&itemFilter(" + x.toString() + ").name=ReturnsAcceptedOnly&itemFilter(" + x.toString() + ").value=true"
//            x += 1
//      }
//      if(req.query.free != 'false'){
//        url = url + "&itemFilter(" + x.toString() + ").name=FreeShippingOnly&itemFilter(" + x.toString() + ").value=true"
//            x += 1
//      }
//      if(req.query.expedited != 'false'){
//        url = url + "&itemFilter(" + x.toString() + ").name=Expedited&itemFilter(" + x.toString() + ").value=true"
//            x += 1
//      }
      if(req.query.new != 'false' || req.query.good != 'false' || req.query.very_good != 'false' || req.query.used != 'false' || req.query.acceptable!= 'false'){
        url = url + "&itemFilter(" + x.toString() + ").name=Condition";
        var x2 = 0;
        if(req.query.new != 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=1000";
            x2 = x2 + 1;
        }
        if(req.query.used!= 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=2000";
            x2 = x2 + 1;
        }
        if(req.query.very_good != 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=3000";
            x2 = x2 + 1;
        }
        if(req.query.good != 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=4000";
            x2 = x2 + 1;
        }
        if(req.query.acceptable != 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=5000";
            x2 = x2 + 1;
        }
        if(req.query.unspecified != 'false'){
            url = url + "&itemFilter(" + x.toString() + ").value(" + x2.toString() + ")=Unspecified";
        }
      }
  }
  var body;
  body = await axios.get(url);
  console.log(body.data);
  res.send(body.data);
})

const PORT = process.env.PORT || 8080;
app.listen(PORT, ()=>{
    console.log(`App on port ${PORT}`);
})
module.exports = app;