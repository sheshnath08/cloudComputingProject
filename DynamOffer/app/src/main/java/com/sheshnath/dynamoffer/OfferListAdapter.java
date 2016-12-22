package com.sheshnath.dynamoffer;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONObject;
import java.io.BufferedWriter;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

/**
 * Created by sheshnath on 11/17/2016.
 */

public class OfferListAdapter extends RecyclerView.Adapter<OfferListAdapter.ViewHolder> {

    private final LayoutInflater mInflater;
    private final List<OfferModel> mFeedList;
    public OfferListAdapter(Context context, List<OfferModel> models) {
        mInflater = LayoutInflater.from(context);
        mFeedList = models;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        final View itemView = mInflater.inflate(R.layout.single_offer_view, parent, false);
        return new ViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, int position) {
        final OfferModel model = mFeedList.get(position);
        holder.offerMerachantName.setText(model.getMerchantName());
        holder.offerDescription.setText(model.getDescription());
        holder.offerClaimButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String offer_id = model.getOfferID();
                SharedPreferences sharedPref = Constants.mainActivityContext.getSharedPreferences(
                        "com.sheshnath.dynamoffer.PREF_FILE",Context.MODE_PRIVATE);
                String user_id = sharedPref.getString("User_ID","null");
                Log.i("userID from claim:",user_id+" "+offer_id);
                if(!user_id.equals("null")) {
                    new ClaimOfferTask(user_id,offer_id, holder.offerClaimButton).execute();
                }
            }
        });
//        holder.bind();
    }

    @Override
    public int getItemCount() {
        if (mFeedList==null){
            return 0;
        }
        return mFeedList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        // each data item is just a string in this case
        private final TextView offerDescription;
        private final TextView offerMerachantName;
        private final Button offerClaimButton;

        public ViewHolder(View itemView) {
            super(itemView);
            offerDescription = (TextView) itemView.findViewById(R.id.offer_description);
            offerMerachantName = (TextView) itemView.findViewById(R.id.offer_merchant_name);
            offerClaimButton = (Button) itemView.findViewById(R.id.offer_claim_button);
            offerClaimButton.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            if (view.getId() == offerClaimButton.getId()) {

                Toast.makeText(view.getContext(), "Comment  "+String.valueOf(getAdapterPosition()) , Toast.LENGTH_SHORT).show();

            }
        }

//        public void bind()
//        {
//            offerDescription.setText("This if offer Description");
//            offerMerachantName.setText("Merchant Name here");
//        }
    }

    class ClaimOfferTask extends AsyncTask<Void, Void, Boolean>{
        String mUserId;
        String mOfferId;
        Button mOfferClaimButton;
        public ClaimOfferTask(String userid, String  offerid, Button offerClaim){
            mUserId = userid;
            mOfferId = offerid;
            mOfferClaimButton = offerClaim;
        }
        @Override
        protected Boolean doInBackground(Void... voids) {
            JSONObject data  = new JSONObject();
            try{
                data.put("userId",mUserId);
                data.put("offerId",mOfferId);
                Log.d("offer Claim Data",data.toString());
                URL url = new URL(Constants.OFFER_CLAIMS);
                int res= HelperClass.doPostRequest(url,data);
                if (res == HttpURLConnection.HTTP_OK){
                    return true;
                }
                Log.i("Response: Claim : ",res+" ");
                // Get the server response
            }
            catch (Exception e){
                Log.e("Login Error:",e.toString());
            }
            return false;
        }

        @Override
        protected void onPostExecute(Boolean aBoolean) {
            super.onPostExecute(aBoolean);
            if(aBoolean){
                mOfferClaimButton.setVisibility(View.INVISIBLE);
            }
        }
    }
}
