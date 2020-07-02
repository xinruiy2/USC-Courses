package com.example.myapplication;

import android.content.Intent;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.tabs.TabLayout;

import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.example.myapplication.ui.main.SectionsPagerAdapter;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class CardActivity extends AppCompatActivity {
    private String item_url;
    private JSONObject jsonString;
    private Bundle bundle;
    private static ProgressBar progressBar;
    private static TextView textUnderProgressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cardview);
        progressBar = findViewById(R.id.progressBar);
        textUnderProgressBar = findViewById(R.id.progressBarWord);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        bundle = getIntent().getExtras();
        String item_id = bundle.getString("item_id");
        String baseURL = "https://nodejs0.wm.r.appspot.com/?productID=" + item_id;
        System.out.println(baseURL);

        String title = bundle.getString("title");
        item_url = bundle.getString("item_url");
        getSupportActionBar().setTitle(title);

        new GetDataTask().execute(baseURL);

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
            try {
                jsonString = new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            progressBar.setVisibility(View.GONE);
            textUnderProgressBar.setVisibility(View.GONE);


            SectionsPagerAdapter sectionsPagerAdapter = new SectionsPagerAdapter(CardActivity.this, getSupportFragmentManager(),jsonString, bundle);
            ViewPager viewPager = findViewById(R.id.view_pager);
            viewPager.setAdapter(sectionsPagerAdapter);
            TabLayout tabs = findViewById(R.id.tabs);
            tabs.setupWithViewPager(viewPager);
            tabs.getTabAt(0).setIcon(R.drawable.information_variant_selected);
            tabs.getTabAt(1).setIcon(R.drawable.ic_seller_blue);
            tabs.getTabAt(2).setIcon(R.drawable.truck_delivery_selected);

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


    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.menubar,menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            onBackPressed();
            return true;
        }
        if(item.getItemId() == R.id.action_favorite){
            Intent launchBrowser = new Intent(Intent.ACTION_VIEW);
            launchBrowser.setData(Uri.parse(item_url));
            startActivity(launchBrowser);
            return true;
        }
        return false;
    }

}