package com.example.myapplication;

import android.graphics.Typeface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.bumptech.glide.Glide;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

public class Tab1 extends Fragment {

    private JSONObject jsonString;
    private Bundle bundle;


    public Tab1(JSONObject mjsonString, Bundle mbundle){
        jsonString = mjsonString;
        bundle = mbundle;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.activity_card1, container, false);

        JSONObject item = new JSONObject();
        try {
            item = jsonString.getJSONObject("Item");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        ImageView image1 = rootView.findViewById(R.id.image1);
        ImageView image2 = rootView.findViewById(R.id.image2);
        ImageView image3 = rootView.findViewById(R.id.image3);
        ImageView image4 = rootView.findViewById(R.id.image4);
        ImageView image5 = rootView.findViewById(R.id.image5);

        TextView price = rootView.findViewById(R.id.itemPrice);
        TextView brand = rootView.findViewById(R.id.BrandRet);
        TextView seeDetails1 = rootView.findViewById(R.id.seeDetails1);
        TextView seeDetails2 = rootView.findViewById(R.id.seeDetails2);
        TextView seeDetails3 = rootView.findViewById(R.id.seeDetails3);
        TextView seeDetails4 = rootView.findViewById(R.id.seeDetails4);
        TextView seeDetails5 = rootView.findViewById(R.id.seeDetails5);

        TextView title = rootView.findViewById(R.id.itemTitle);
        TextView shippingBefore = rootView.findViewById(R.id.shippingBefore);
        TextView shipping = rootView.findViewById(R.id.shipping);
        TextView shippingAfter = rootView.findViewById(R.id.shippingAfter);

        try {
            price.setText("$" + item.getJSONObject("CurrentPrice").getString("Value"));
            price.setTypeface(null, Typeface.BOLD);
        } catch (JSONException e) {
        }

        try {
            Glide.with(this).load(item.getJSONArray("PictureURL").getString(0)).into(image1);
        } catch (JSONException e) {
        }

        try {
            Glide.with(this).load(item.getJSONArray("PictureURL").getString(1)).into(image2);
        } catch (JSONException e) {
        }

        try {
            Glide.with(this).load(item.getJSONArray("PictureURL").getString(2)).into(image3);
        } catch (JSONException e) {
        }

        try {
            Glide.with(this).load(item.getJSONArray("PictureURL").getString(3)).into(image4);
        } catch (JSONException e) {
        }

        try {
            Glide.with(this).load(item.getJSONArray("PictureURL").getString(4)).into(image5);
        } catch (JSONException e) {
        }

        try{
            brand.setText(item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(0).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        try {
            seeDetails1.setText("•" +item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(1).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        try {
            seeDetails2.setText("•" +item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(2).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        try {
            seeDetails3.setText("•" +item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(3).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        try {
            seeDetails4.setText("•" +item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(4).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        try {
            seeDetails5.setText("•" + item.getJSONObject("ItemSpecifics").getJSONArray("NameValueList").getJSONObject(5).getJSONArray("Value").getString(0));
        } catch (JSONException e) {
        }

        title.setText(bundle.getString("title"));
        title.setTypeface(null, Typeface.BOLD);

        if(bundle.getString("shipCost").equals("Free")){
            shipping.setText("Free");
            shipping.setVisibility(View.VISIBLE);
            shipping.setTypeface(null, Typeface.BOLD);
            shippingAfter.setVisibility(View.VISIBLE);
        }else{
            shippingBefore.setVisibility(View.VISIBLE);
            shipping.setText(bundle.getString("shipCost"));
            shipping.setVisibility(View.VISIBLE);
            shipping.setTypeface(null, Typeface.BOLD);
        }

        return rootView;
    }

}
