package com.sheshnath.dynamoffer.Activity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Parcelable;
import android.os.PersistableBundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.widget.Toast;

import com.sheshnath.dynamoffer.Constants;
import com.sheshnath.dynamoffer.OfferListAdapter;
import com.sheshnath.dynamoffer.OfferModel;
import com.sheshnath.dynamoffer.R;

import org.apache.http.params.CoreConnectionPNames;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by sheshnath on 12/12/2016.
 */

public class RecommendedOfferActivity extends AppCompatActivity {
    private RecyclerView mRecommendedRecyclerView;
    private List<OfferModel> recomendedOfferList;
    private static Parcelable recommendedViewState = null;
    OfferListAdapter mRecommendedAdapter;


    @Override
    public void onCreate(Bundle savedInstanceState, PersistableBundle persistentState) {
        super.onCreate(savedInstanceState, persistentState);
        setContentView(R.layout.recommended_activity_layout);
        mRecommendedRecyclerView = (RecyclerView) findViewById(R.id.recommend_list_view);
        mRecommendedRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        if(recommendedViewState !=null){
            Log.d("recycler state",recommendedViewState+"");
            mRecommendedRecyclerView.getLayoutManager().onRestoreInstanceState(recommendedViewState);
        }
        SharedPreferences sharedPref = getSharedPreferences(
                getString(R.string.preference_file_key), Context.MODE_PRIVATE);
        String user_id = sharedPref.getString("User_ID","null");
        String lat = sharedPref.getString("lat","null");
        String lon = sharedPref.getString("lon","null");
        new FetchRecomendedOfferTask(user_id,lat,lon).execute();
    }

    @Override
    protected void onStart() {
        super.onStart();
        setContentView(R.layout.recommended_activity_layout);
        mRecommendedRecyclerView = (RecyclerView) findViewById(R.id.recommend_list_view);
        mRecommendedRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        if(recommendedViewState !=null){
            Log.d("recycler state",recommendedViewState+"");
            mRecommendedRecyclerView.getLayoutManager().onRestoreInstanceState(recommendedViewState);
        }
        SharedPreferences sharedPref = getSharedPreferences(
                getString(R.string.preference_file_key), Context.MODE_PRIVATE);
        String user_id = sharedPref.getString("User_ID","null");
        String lat = sharedPref.getString("lat","null");
        String lon = sharedPref.getString("lon","null");
        new FetchRecomendedOfferTask(user_id,lat,lon).execute();
    }

    class FetchRecomendedOfferTask extends AsyncTask<Void,Void, Integer> {
        String mUserId;
        String mLat;
        String mLng;
        int result = 0;
        public FetchRecomendedOfferTask(String userId, String lat, String lng){
            mUserId = userId;
            mLat = lat;
            mLng = lng;
        }
        @Override
        protected Integer doInBackground(Void... voids) {
            try {
//                lat=40.2454&lon=-40.45678&maxdist=5000&userId=58533df136e8b80e043b7e3d
                String link = Constants.RECOMMENDED_OFFER_URL+"lat="+mLat+"&lon="+mLng+"&maxdist=5000&userId="+mUserId;
                Log.d("URL",link);
                URL url = new URL(link);
//TODO: Update Offer_URL with Recommended url
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                int responseCode=conn.getResponseCode();
                Log.i("Recomm",responseCode+"");
                Log.i("Conn: ",conn.getRequestMethod());
                if (responseCode == 200) {
                    BufferedReader r = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = r.readLine()) != null) {
                        response.append(line);
                    }
                    result = 1; // Successful
                } else {
                    result = 0; //"Failed to fetch data!";
                }
            } catch (ProtocolException e1) {
                e1.printStackTrace();
            } catch (MalformedURLException e1) {
                e1.printStackTrace();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            return result;
        }

        @Override
        protected void onPostExecute(Integer result) {
            if (result == 1) {
                Context context = getBaseContext();
                mRecommendedAdapter = new OfferListAdapter(context, recomendedOfferList);
                mRecommendedRecyclerView.setAdapter(mRecommendedAdapter);
            } else {
                Toast.makeText(RecommendedOfferActivity.this, "Failed to fetch data!", Toast.LENGTH_SHORT).show();
            }
        }
    }

//    private void parseResult(String s){
//        Log.d("Recomm",s);
//            try {
//                JSONObject response = new JSONObject(s);
//                JSONArray posts = response.optJSONArray("response");
//                recomendedOfferList = new ArrayList<>();
//                for (int i = 0; i < posts.length(); i++) {
//                    JSONObject post = posts.optJSONObject(i);
//                    OfferModel item = new OfferModel();
//                    item.setDescription(post.optString("description"));
//                    item.setMerchantName(post.optString("merchantId"));
//                    item.setOfferID(post.optString("offerId"));
//                    recomendedOfferList.add(item);
//                }
//            } catch (JSONException e) {
//                e.printStackTrace();
//            }
//    }
}
