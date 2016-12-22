package com.sheshnath.dynamoffer.Activity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Parcelable;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.location.LocationRequest;
import com.sheshnath.dynamoffer.Constants;
import com.sheshnath.dynamoffer.FilterSettingActivity;
import com.sheshnath.dynamoffer.HelperClass;
import com.sheshnath.dynamoffer.LocationUtils.LocationService;
import com.sheshnath.dynamoffer.LocationUtils.SmartLocationManager;
import com.sheshnath.dynamoffer.OfferListAdapter;
import com.sheshnath.dynamoffer.OfferModel;
import com.sheshnath.dynamoffer.R;

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


public class MainActivity extends AppCompatActivity implements
        NavigationView.OnNavigationItemSelectedListener {
    OfferListAdapter mAdapter;
    private RecyclerView mRecyclerView;
    private static Parcelable recyclerViewState = null;
    private List<OfferModel> offerFeedList;
    public static final String TAG = MainActivity.class.getSimpleName();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Context context = getBaseContext();
        SharedPreferences sharedPreferences = context.getSharedPreferences(
                getString(R.string.preference_file_key), Context.MODE_PRIVATE);
        Boolean isLoggedIn = sharedPreferences.getBoolean(getString(R.string.is_logged_in), false);
        if (!isLoggedIn) {
            finish();
            startLoginActivity();
        }
        Constants.mainActivityContext = getApplicationContext();
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
//        mNavUserName = (TextView)drawer.findViewById(R.id.nav_user_name);
//        String name = sharedPreferences.getString("name","No Name");
//        mNavUserName.setText(name);
        drawer.setDrawerListener(toggle);
        toggle.syncState();
        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        // setting list view here
        mRecyclerView=(RecyclerView)findViewById(R.id.offer_list_view);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        if(recyclerViewState !=null){
            Log.d("recycler state",recyclerViewState+"");
            mRecyclerView.getLayoutManager().onRestoreInstanceState(recyclerViewState);
        }
        new FetchFeaturedOfferTask("id","lat","lng").execute();

        Intent intent = new Intent(this,LocationService.class);
        startService(intent);
    }
    protected void onStart() {
        super.onStart();

    }

    protected void onStop() {
        super.onStop();
    }

    @Override
    protected void onPause() {
        super.onPause();

    }

//    for broadcast receiver
    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

    private void startLoginActivity() {
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
    }

    private void startFilterSettingActivity() {
        Intent intent = new Intent(this, FilterSettingActivity.class);
        startActivity(intent);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startFilterSettingActivity();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

       if (id == R.id.nav_recomm_offer) {
            startRecommendedOfferActivity();

        } else if (id == R.id.nav_logout) {
            Context context = getBaseContext();
            SharedPreferences sharedPreferences =
                    context.getSharedPreferences(getString(R.string.preference_file_key), Context.MODE_PRIVATE);
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putBoolean(getString(R.string.is_logged_in), false);
            editor.commit();
            finish();
            startLoginActivity();

        } else if (id == R.id.nav_share) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    private void startRecommendedOfferActivity() {
        Intent intent = new Intent(this,RecommendedOfferActivity.class);
        startActivity(intent);
    }


    class FetchFeaturedOfferTask extends AsyncTask<Void, Void, Integer>{

        String mUserId;
        String mLat;
        String mLng;
        int result = 0;
        FetchFeaturedOfferTask(String userid, String lat, String lng){
            mUserId = userid;
            mLat = lat;
            mLng = lng;
        }
        @Override
        protected Integer doInBackground(Void... voids) {
            try {
                URL url = new URL(Constants.OFFER_URL);

                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                int responseCode=conn.getResponseCode();
                Log.i("ResponseCode",responseCode+"");
                Log.i("Conn: ",conn.getRequestMethod());
                if (responseCode == 200) {
                    BufferedReader r = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = r.readLine()) != null) {
                        response.append(line);
                    }
                    parseResult(response.toString(),0);
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
                mAdapter = new OfferListAdapter(context, offerFeedList);
                mRecyclerView.setAdapter(mAdapter);
            } else {
                Toast.makeText(MainActivity.this, "Failed to fetch data!", Toast.LENGTH_SHORT).show();
            }
        }
    }


        private void parseResult(String s, int type) {
            Log.i("Result:",s);
            if(type == 0){
                try {
                    JSONObject response = new JSONObject(s);
                    JSONArray posts = response.optJSONArray("response");
                    offerFeedList = new ArrayList<>();
                    for (int i = 0; i < posts.length(); i++) {
                        JSONObject post = posts.optJSONObject(i);
                        OfferModel item = new OfferModel();
                        item.setDescription(post.optString("description"));
                        item.setMerchantName(post.optString("merchantId"));
                        item.setMerchantName(post.optString("name"));
                        item.setOfferID(post.optString("_id"));
                        offerFeedList.add(item);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

        }
}