package com.example.myapplication;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
import android.os.Handler;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.Buffer;
import java.util.ArrayList;

public class ResultActivity extends AppCompatActivity {
    //    private TextView mResult;
    private JSONObject recieved_json;
    String baseURL;
    private String keyword_name;
    private static final String TAG = "mainActivity";

    SwipeRefreshLayout refreshLayout;
    RelativeLayout relativeLayout;

    private ArrayList<String> image_list = new ArrayList<String>();
    private ArrayList<String> title_list = new ArrayList<String>();
    private ArrayList<String> condition_list = new ArrayList<String>();
    private ArrayList<String> shipping_list = new ArrayList<String>();
    private ArrayList<String> price_list = new ArrayList<String>();
    private ArrayList<String> topRate_list = new ArrayList<String>();
    private ArrayList<String> item_id_list = new ArrayList<>();
    private ArrayList<String> item_url_list = new ArrayList<>();

    private ArrayList<String> expedited_list = new ArrayList<>();
    private ArrayList<String> shippingTo_list = new ArrayList<>();
    private ArrayList<String> shippingFrom_list = new ArrayList<>();
    private ArrayList<String> oneDay_list = new ArrayList<>();
    private ArrayList<String> shippingType_list = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        refreshLayout = findViewById(R.id.swiperefresh);
        relativeLayout = findViewById(R.id.relativeLayout);

        refreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                relativeLayout.setVisibility(View.GONE);
                final Handler handler = new Handler();
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        if(refreshLayout.isRefreshing()) {
                            refreshLayout.setRefreshing(false);
                            relativeLayout.setVisibility(View.VISIBLE);
                        }
                    }
                }, 1500);
            }
        });

        Bundle bundle = getIntent().getExtras();
        String URL = bundle.getString("URL");
        baseURL = bundle.getString("URL");
        keyword_name = bundle.getString("keyword");

        System.out.println(baseURL);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        new GetDataTask().execute(URL);

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            onBackPressed();
            return true;
        }
        return false;
    }



    class GetDataTask extends AsyncTask<String,Void,String> {


        @Override
        protected void onPreExecute(){

            super.onPreExecute();

        }

        @Override
        protected String doInBackground(String... params) {
            try {
                return getData(params[0]);
            } catch (IOException | JSONException e) {
                return "Network error!";
            }
        }

        @Override
        protected void onPostExecute(String result){
            super.onPostExecute(result);


//            result contains the json data
            try {
                recieved_json = new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            JSONObject item = new JSONObject();

            try {
                item = recieved_json.getJSONArray("findItemsAdvancedResponse").getJSONObject(0).getJSONArray("searchResult").getJSONObject(0);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            String count = "0";
            try {
                count = item.getString("@count");
            } catch (JSONException e) {
                e.printStackTrace();
            }

            if(count.equals("0")){
                ProgressBar progressBar = findViewById(R.id.progressBar);
                progressBar.setVisibility(View.GONE);
                TextView progressBarWord = findViewById(R.id.progressBarWord);
                progressBarWord.setVisibility(View.GONE);
                TextView nresult = (TextView) findViewById(R.id.noResults);
                nresult.setVisibility(View.VISIBLE);
                Toast.makeText(getApplicationContext(),"No Records",Toast.LENGTH_LONG).show();
            }else{
                TextView l1 =  (TextView) findViewById(R.id.line_1);
                TextView l2 =  (TextView) findViewById(R.id.line_2);
                TextView l3 =  (TextView) findViewById(R.id.line_3);
                TextView l4 =  (TextView) findViewById(R.id.line_4);
                l2.setText(count);
                l4.setText(keyword_name);
                l1.setVisibility(View.VISIBLE);
                l2.setVisibility(View.VISIBLE);
                l3.setVisibility(View.VISIBLE);
                l4.setVisibility(View.VISIBLE);


                for(int i = 0; i<Integer.parseInt(count); i++){
                    try {
                        title_list.add((String)item.getJSONArray("item").getJSONObject(i).getJSONArray("title").getString(0));
                    } catch (JSONException e) {
                        title_list.add("Unknown title");
                    }

                    try {
                        image_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("galleryURL").getString(0));
                    } catch (JSONException e) {
//                        title_list.set(i, "");
                    }

                    String shipping_service_type;

                    try {
                        shipping_service_type = item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("shippingType").getString(0);
                    } catch (JSONException e) {
                        shipping_service_type = "Free";
                    }
                    if(shipping_service_type.equals("Free"))    shipping_list.add("Free");
                    else{
                        try {
                            shipping_list.add("$" + item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("shippingServiceCost").getJSONObject(0).getString("__value__"));
                        } catch (JSONException e) {
                            shipping_list.add("Free");
                        }
                    }

                    try {
                        condition_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("condition").getJSONObject(0).getJSONArray("conditionDisplayName").getString(0));
                    } catch (JSONException e) {
                        condition_list.add("N/A");
                    }

                    try {
                        price_list.add("$"+item.getJSONArray("item").getJSONObject(i).getJSONArray("sellingStatus").getJSONObject(0).getJSONArray("currentPrice").getJSONObject(0).getString("__value__"));
                    } catch (JSONException e) {
                        price_list.add("$0.0");
                    }

                    String rate;
                    try{
                        rate = item.getJSONArray("item").getJSONObject(i).getJSONArray("topRatedListing").getString(0);
                    } catch (JSONException e) {
                        rate = "false";
                    }
                    if(rate.equals("true")) topRate_list.add("Top Rate Listing");
                    else topRate_list.add("");

                    try {
                        item_id_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("itemId").getString(0));
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    try {
                        item_url_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("viewItemURL").getString(0));
                    } catch (JSONException e) {
                        item_url_list.add("https://www.ebay.com/");
                    }

                    try {
                        expedited_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("expeditedShipping").getString(0));
                    } catch (JSONException e) {
                        expedited_list.add("false");
                    }

                    try {
                        shippingTo_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("shipToLocations").getString(0));
                    } catch (JSONException e) {
                        shippingTo_list.add("Not Specified");
                    }

                    try {
                        shippingFrom_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("location").getString(0));
                    } catch (JSONException e) {
                        shippingFrom_list.add("Not Specified");
                    }

                    try {
                        oneDay_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("oneDayShippingAvailable").getString(0));
                    } catch (JSONException e) {
                        oneDay_list.add("false");
                    }

                    try {
                        shippingType_list.add(item.getJSONArray("item").getJSONObject(i).getJSONArray("shippingInfo").getJSONObject(0).getJSONArray("shippingType").getString(0));
                    } catch (JSONException e) {
                        shippingType_list.add("Not Specified");
                    }


                    initView();
                }
            }

        }

        private String getData(String urlPath) throws IOException, JSONException {
            StringBuilder result = new StringBuilder();
            BufferedReader bufferedReader = null;

            try{
                URL url = new URL(urlPath);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setReadTimeout(10000);
                urlConnection.setConnectTimeout(10000);
                urlConnection.setRequestMethod("GET");
                urlConnection.setRequestProperty("Content-Type", "application/json");
                urlConnection.connect();

//                read data response from server
                InputStream inputStream = urlConnection.getInputStream();
                bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                String line;
                while((line = bufferedReader.readLine())!= null){
                    result.append(line).append("\n");
                }

            } finally{
                if(bufferedReader != null){
                    bufferedReader.close();
                }
            }

            return result.toString();
        }

    }

    private void initView(){
        Log.d(TAG,"Preparing now:");
        RecyclerView recyclerView = findViewById(R.id.my_recycler_view);
        RecyclerViewAdapter adpter = new RecyclerViewAdapter(expedited_list, shippingFrom_list, shippingTo_list, shippingType_list, oneDay_list,baseURL,item_url_list,item_id_list,image_list,title_list,condition_list,shipping_list,price_list,topRate_list,this);
        recyclerView.setAdapter(adpter);
        recyclerView.setLayoutManager(new GridLayoutManager(this,2));
        ProgressBar progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.GONE);
        TextView progressBarWord = findViewById(R.id.progressBarWord);
        progressBarWord.setVisibility(View.GONE);

    }
}
