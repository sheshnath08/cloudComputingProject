package com.sheshnath.dynamoffer.Notification;

import android.content.Context;
import android.content.SharedPreferences;
import android.support.v7.widget.ThemedSpinnerAdapter;
import android.util.Log;

import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.FirebaseInstanceIdService;
import com.sheshnath.dynamoffer.Constants;
import com.sheshnath.dynamoffer.HelperClass;
import com.sheshnath.dynamoffer.R;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URL;

/**
 * Created by sheshnath on 12/8/2016.
 */

public class MyFirebaseInstanceIDService extends FirebaseInstanceIdService {
    private static String TAG = "MyFirebaseIDService";

    @Override
    public void onTokenRefresh() {
        // Get updated InstanceID token.
        String refreshedToken = FirebaseInstanceId.getInstance().getToken();
        Log.d(TAG, "Refreshed token: " + refreshedToken);

        // If you want to send messages to this application instance or
        // manage this apps subscriptions on the server side, send the
        // Instance ID token to your app server.
        SharedPreferences sharedPref = getSharedPreferences(
                getString(R.string.preference_file_key),Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPref.edit();
        editor.putString(Constants.firebase_token,refreshedToken);
        editor.commit();
//        HelperClass.sendRegistrationToServer(refreshedToken,sharedPref);
    }




}
