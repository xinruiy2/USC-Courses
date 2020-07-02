package com.example.myapplication;

import android.graphics.Typeface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

public class Tab3 extends Fragment {

    TextView HandlingTime;
    TextView OneDayShipping;
    TextView ShippingType;
    TextView ShippingFrom;
    TextView ShippingTo;
    TextView ExpeditedShipping;
    JSONObject jsonString;
    private Bundle bundle;


    public Tab3(JSONObject mjsonString, Bundle mbundle){
        jsonString = mjsonString;
        bundle = mbundle;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.activity_card3, container, false);
        JSONObject item = new JSONObject();
        try {
            item = jsonString.getJSONObject("Item");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        HandlingTime = rootView.findViewById(R.id.HandlingTime);
        OneDayShipping = rootView.findViewById(R.id.OneDayShipping);
        ShippingType = rootView.findViewById(R.id.shippingType);
        ShippingFrom = rootView.findViewById(R.id.shippingFrom);
        ShippingTo = rootView.findViewById(R.id.shippingTo);
        ExpeditedShipping = rootView.findViewById(R.id.expeditedShipping);


        HandlingTime.setTypeface(null, Typeface.BOLD);
        OneDayShipping.setTypeface(null, Typeface.BOLD);
        ShippingType.setTypeface(null, Typeface.BOLD);
        ShippingFrom.setTypeface(null, Typeface.BOLD);
        ShippingTo.setTypeface(null, Typeface.BOLD);
        ExpeditedShipping.setTypeface(null, Typeface.BOLD);

        TextView HandlingtimeRet = rootView.findViewById(R.id.HandlingTimeRet);
        TextView OneDayShippingRet = rootView.findViewById(R.id.OneDayShippingRET);
        TextView shippingTypeRet = rootView.findViewById(R.id.shippingTypeRet);
        TextView shippingFromRet = rootView.findViewById(R.id.shippingFromRet);
        TextView shippingToRet = rootView.findViewById(R.id.ShippingToRet);
        TextView expeditedShipping = rootView.findViewById(R.id.expeditedShippingRet);

        try {
            HandlingtimeRet.setText(item.getString("HandlingTime"));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        OneDayShippingRet.setText(bundle.getString("oneDay"));
        shippingTypeRet.setText(bundle.getString("shipType"));
        shippingFromRet.setText(bundle.getString("shipFrom"));
        shippingToRet.setText(bundle.getString("shipTo"));
        expeditedShipping.setText(bundle.getString("expedited"));

        return rootView;
    }

}
