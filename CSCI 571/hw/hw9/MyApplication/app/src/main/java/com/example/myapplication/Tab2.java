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

public class Tab2 extends Fragment {

    TextView Feedback;
    TextView User_ID;
    TextView PositveFeedback;
    TextView FeedbackRate;
    TextView Refund;
    TextView ReturnWithin;
    TextView ShippingCostPaid;
    TextView ReturnAccepted;

    TextView FeedbackRet;
    TextView User_IDRet;
    TextView PositveFeedbackRet;
    TextView FeedbackRateRet;
    TextView RefundRet;
    TextView ReturnWithinRet;
    TextView ShippingCostPaidRet;
    TextView ReturnAcceptedRet;

    JSONObject jsonString;

    public Tab2(JSONObject mjsonString){
        jsonString = mjsonString;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.activity_card2, container, false);

        JSONObject item = new JSONObject();
        try {
            item = jsonString.getJSONObject("Item");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        Feedback = rootView.findViewById(R.id.Feedback);
        User_ID = rootView.findViewById(R.id.UserID);
        PositveFeedback = rootView.findViewById(R.id.PositiveFeedback);
        FeedbackRate = rootView.findViewById(R.id.FeedbackRate);
        Refund = rootView.findViewById(R.id.Refund);
        ReturnWithin = rootView.findViewById(R.id.returnWithin);
        ShippingCostPaid = rootView.findViewById(R.id.ShippingCostPaid);
        ReturnAccepted = rootView.findViewById(R.id.returnAccept);

        Feedback.setTypeface(null, Typeface.BOLD);
        User_ID.setTypeface(null, Typeface.BOLD);
        PositveFeedback.setTypeface(null, Typeface.BOLD);
        FeedbackRate.setTypeface(null, Typeface.BOLD);
        Refund.setTypeface(null, Typeface.BOLD);
        ReturnWithin.setTypeface(null, Typeface.BOLD);
        ShippingCostPaid.setTypeface(null, Typeface.BOLD);
        ReturnAccepted.setTypeface(null, Typeface.BOLD);

        FeedbackRet = rootView.findViewById(R.id.FeedbackRet);
        User_IDRet = rootView.findViewById(R.id.UserIDRet);
        PositveFeedbackRet = rootView.findViewById(R.id.PositiveFeedbackRet);
        FeedbackRateRet = rootView.findViewById(R.id.FeedbackRateRet);
        ReturnWithinRet = rootView.findViewById(R.id.returnWithinRet);
        ReturnAcceptedRet = rootView.findViewById(R.id.returnAcceptRet);
        ShippingCostPaidRet = rootView.findViewById(R.id.ShippingCostPaidRet);
        RefundRet = rootView.findViewById(R.id.RefundRet);

        try {
            FeedbackRet.setText(item.getJSONObject("Seller").getString("FeedbackScore"));
        } catch (JSONException e) {
        }

        try {
            User_IDRet.setText(item.getJSONObject("Seller").getString("UserID"));
        } catch (JSONException e) {
        }

        try {
            PositveFeedbackRet.setText(item.getJSONObject("Seller").getString("PositiveFeedbackPercent"));
        } catch (JSONException e) {
        }

        try {
            FeedbackRateRet.setText(item.getJSONObject("Seller").getString("FeedbackRatingStar"));
        } catch (JSONException e) {
        }

        try {
            ReturnWithinRet.setText(item.getJSONObject("ReturnPolicy").getString("ReturnsWithin"));
        } catch (JSONException e) {
        }

        try {
            ReturnAcceptedRet.setText(item.getJSONObject("ReturnPolicy").getString("ReturnsAccepted"));
        } catch (JSONException e) {
        }

        try {
            ShippingCostPaidRet.setText(item.getJSONObject("ReturnPolicy").getString("ShippingCostPaidBy"));
        } catch (JSONException e) {
        }

        try {
            RefundRet.setText(item.getJSONObject("ReturnPolicy").getString("Refund"));
        } catch (JSONException e) {
        }


        return rootView;
    }
}
