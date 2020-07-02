package com.example.myapplication;

import android.content.Context;
import android.content.Intent;
import android.graphics.Typeface;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;

import java.util.ArrayList;

public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewAdapter.ViewHolder>{

    private static final String TAG="RecyclerViewAdapter";
    private String baseURL;
    private ArrayList<String> item_id_list = new ArrayList<>();
    private ArrayList<String> image_list = new ArrayList<>();
    private ArrayList<String> title_list = new ArrayList<>();
    private ArrayList<String> condition_list = new ArrayList<>();
    private ArrayList<String> shipping_list = new ArrayList<>();
    private ArrayList<String> price_list = new ArrayList<>();
    private ArrayList<String> topRate_list = new ArrayList<>();
    private ArrayList<String> item_url_list = new ArrayList<>();

    private ArrayList<String> expedited_list = new ArrayList<>();
    private ArrayList<String> shippingTo_list = new ArrayList<>();
    private ArrayList<String> shippingFrom_list = new ArrayList<>();
    private ArrayList<String> oneDay_list = new ArrayList<>();
    private ArrayList<String> shippingType_list = new ArrayList<>();

    private Context mContext;

    public RecyclerViewAdapter(ArrayList<String> mexpedited_list,ArrayList<String> mshippingFrom_list,ArrayList<String> mshippingTo_list,ArrayList<String> mshippingType_list,ArrayList<String> moneDay_list,String url, ArrayList<String> mitem_url_list, ArrayList<String> mitem_id_list, ArrayList<String> img_list, ArrayList<String> tit_list, ArrayList<String> cond_list, ArrayList<String> ship_list, ArrayList<String> pri_list, ArrayList<String> top_list, Context context){
        expedited_list = mexpedited_list;
        shippingTo_list = mshippingTo_list;
        shippingFrom_list = mshippingFrom_list;
        oneDay_list = moneDay_list;
        shippingType_list = mshippingType_list;
        baseURL = url;
        item_url_list = mitem_url_list;
        item_id_list = mitem_id_list;
        image_list = img_list;
        title_list = tit_list;
        condition_list = cond_list;
        shipping_list = ship_list;
        price_list = pri_list;
        topRate_list = top_list;
        mContext = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_recard, parent, false);
        ViewHolder holder = new ViewHolder(view);
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, final int position) {
        Log.d(TAG, "onBindViewHolder: called.");

        if(!image_list.get(position).equals("https://thumbs1.ebaystatic.com/pict/04040_0.jpg")){
            Glide.with(mContext)
                    .asBitmap()
                    .load(image_list.get(position))
                    .into(holder.image);
        }

        holder.condition.setText(condition_list.get(position));
        if(shipping_list.get(position).equals("Free")){
            holder.shippingbefore.setVisibility(View.GONE);
            holder.shipping.setText(shipping_list.get(position));
            holder.shippingafter.setVisibility(View.VISIBLE);
        }else{
            holder.shippingafter.setVisibility(View.GONE);
            holder.shippingbefore.setVisibility(View.VISIBLE);
            holder.shipping.setText(shipping_list.get(position));
        }
        holder.price.setText(price_list.get(position));
        holder.topRate.setText(topRate_list.get(position));
        holder.title.setText(title_list.get(position));


        holder.parentLayout.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                System.out.println(position);
                Intent intent = new Intent(mContext, CardActivity.class);
                intent.putExtra("URL", baseURL);
                intent.putExtra("item_id", item_id_list.get(position));
                intent.putExtra("title", title_list.get(position));
                intent.putExtra("oneDay", oneDay_list.get(position));
                intent.putExtra("shipTo", shippingTo_list.get(position));
                intent.putExtra("shipFrom",shippingFrom_list.get(position));
                intent.putExtra("expedited",expedited_list.get(position));
                intent.putExtra("item_url",item_url_list.get(position));
                intent.putExtra("shipType", shippingType_list.get(position));
                intent.putExtra("shipCost", shipping_list.get(position));
                mContext.startActivity(intent);
            }
    });

    }

    @Override
    public int getItemCount() {
        return image_list.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder{

        ImageView image;
        TextView  title;
        TextView  shipping;
        TextView  shippingbefore;
        TextView  shippingafter;
        TextView  topRate;
        TextView  condition;
        TextView  price;
        CardView  parentLayout;

        public ViewHolder(View itemView){
            super(itemView);
            parentLayout = itemView.findViewById(R.id.parent_layout);
            image = itemView.findViewById(R.id.image);
            title = itemView.findViewById(R.id.title);
            title.setTypeface(null, Typeface.BOLD);
            shipping = itemView.findViewById(R.id.shipping);
            shipping.setTypeface(null, Typeface.BOLD);
            topRate = itemView.findViewById(R.id.topRate);
            topRate.setTypeface(null, Typeface.BOLD);
            shippingbefore = itemView.findViewById(R.id.shippingBefore);
            shippingafter = itemView.findViewById(R.id.shippingAfter);
            condition = itemView.findViewById(R.id.condition);
            condition.setTypeface(null, Typeface.BOLD_ITALIC);
            price = itemView.findViewById(R.id.price);
        }

    }
}
