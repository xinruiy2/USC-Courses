package com.example.myapplication;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.Spinner;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.List;


public class BasicActivity extends AppCompatActivity {
    private Spinner spinner1;
    private EditText keyword_text, minPrice_text, maxPrice_text;
    private TextView firstWarning, secondWarning;
    private Button buttonSubmit, buttonReset;
    private CheckBox checkBox_new, checkBox_used, checkBox_unknown;
    private boolean ifNew, ifUsed, ifUnknown = false;
    private String spinner_text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        addItemsOnSpinner();

        keyword_text  = (EditText) findViewById(R.id.keywords);
        minPrice_text = (EditText) findViewById(R.id.minPrice);
        maxPrice_text = (EditText) findViewById(R.id.maxPrice);
        firstWarning = (TextView) findViewById(R.id.keywordWarning);
        secondWarning = (TextView) findViewById(R.id.priceWarning);

        firstWarning.setTypeface(null, Typeface.ITALIC);
        secondWarning.setTypeface(null, Typeface.ITALIC);

        buttonSubmit = (Button) findViewById(R.id.submit);
        buttonReset = (Button) findViewById(R.id.clear);

        checkBox_new = (CheckBox) findViewById(R.id.check_new);
        checkBox_used = (CheckBox) findViewById(R.id.check_used);
        checkBox_unknown = (CheckBox) findViewById(R.id.check_unspecified);

//        submit button
        buttonSubmit.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                String keyword = keyword_text.getText().toString();
                String minPrice = minPrice_text.getText().toString();
                String maxPrice = maxPrice_text.getText().toString();

                String baseURL = "https://nodejs0.wm.r.appspot.com/?";

                boolean ifWarned = false;

                firstWarning.setVisibility(View.GONE);
                secondWarning.setVisibility(View.GONE);


                if(keyword.trim().equals("")){
                    firstWarning.setVisibility(View.VISIBLE);
                    Toast.makeText(getApplicationContext(),"Please fills all field with errors",Toast.LENGTH_LONG).show();
                    ifWarned = true;
                }else{
                    baseURL += "keyword=" + keyword;
                }

                if(!maxPrice.trim().equals("")){
                    baseURL += "&maxPrice=" + maxPrice;
                    if(!minPrice.trim().equals("")){
                        if(Float.parseFloat(minPrice) > Float.parseFloat(maxPrice)){
                            secondWarning.setVisibility(View.VISIBLE);
                            if(!ifWarned)   Toast.makeText(getApplicationContext(),"Please fills all field with errors",Toast.LENGTH_LONG).show();
                            ifWarned = true;
                        }
                        baseURL += "&minPrice=" + minPrice;
                    }else{
                        baseURL += "&minPrice=null";
                    }
                }else{
                    baseURL += "&maxPrice=null";
                    if(!minPrice.trim().equals("")){
                        baseURL += "&minPrice=" + minPrice;
                    }else{
                        baseURL += "&minPrice=null";
                    }
                }

                if(ifWarned)    return;

                spinner_text = spinner1.getSelectedItem().toString();

                if (ifNew)  baseURL += "&new=true";
                else    baseURL += "&new=false";
                if (ifUsed)  baseURL += "&used=true";
                else baseURL += "&used=false";
                if (ifUnknown)  baseURL += "&unspecified=true";
                else  baseURL += "&unspecified=false";

                baseURL += "&very_good=false";
                baseURL += "&acceptable=false";
                baseURL += "&good=false";

                if(spinner_text.equals("Best Match"))    baseURL += "&sortOrder=BestMatch";
                else if(spinner_text.equals("Price: Highest first"))    baseURL += "&sortOrder=CurrentPriceHighest";
                else if(spinner_text.equals("Price + Shipping: Highest first")) baseURL += "&sortOrder=PricePlusShippingHighest";
                else if(spinner_text.equals("Price + Shipping: Lowest first"))  baseURL += "&sortOrder=PricePlusShippingLowest";

//                System.out.println(baseURL);
                Intent intent = new Intent(BasicActivity.this, ResultActivity.class);
                intent.putExtra("URL", baseURL);
                intent.putExtra("keyword",keyword);
//                make a api call here to the node.js
                startActivity(intent);
            }
        });

        buttonReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                keyword_text.setText("");
                minPrice_text.setText("");
                maxPrice_text.setText("");
                firstWarning.setVisibility(View.GONE);
                secondWarning.setVisibility(View.GONE);
                ifNew = false;
                ifUsed = false;
                ifUnknown = false;
                spinner1.setSelection(0);
                checkBox_new.setChecked(false);
                checkBox_unknown.setChecked(false);
                checkBox_used.setChecked(false);
            }
        });

    }

    public void onCheckboxClicked(View view) {
        if(checkBox_new.isChecked()){
            ifNew = true;
        }else{
            ifNew = false;
        }

        if(checkBox_used.isChecked()){
            ifUsed = true;
        }else{
            ifUsed = false;
        }

        if(checkBox_unknown.isChecked()){
            ifUnknown = true;
        }else{
            ifUnknown = false;
        }
    }

    public void addItemsOnSpinner() {

        spinner1 = (Spinner) findViewById(R.id.spinner);
        List<String> list = new ArrayList<String>();
        list.add("Best Match");
        list.add("Price: Highest first");
        list.add("Price + Shipping: Highest first");
        list.add("Price + Shipping: Lowest first");
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, list);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner1.setAdapter(dataAdapter);
    }

}