package com.sheshnath.dynamoffer;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by sheshnath on 11/9/2016.
 */

public class HelperClass {
    // General Methods defined here.

    public  static int dosignupPostRequest(URL url, JSONObject data,SharedPreferences pref){
        try {
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            // Set Timeout and method
            conn.setReadTimeout(7000);
            conn.setConnectTimeout(7000);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");
            conn.setDoOutput(true);
            conn.setDoInput(true);

//                conn.addRequestProperty("data",data.toString());
            OutputStream os = conn.getOutputStream();
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(data.toString());
            writer.flush();
            writer.close();
            os.close();
            conn.connect();
            if( conn.getResponseCode() == HttpURLConnection.HTTP_OK){
                BufferedReader r = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = r.readLine()) != null) {
                    response.append(line);
                }
                saveData(response.toString(),pref);
            }
            return conn.getResponseCode();
        }
        catch (Exception e){
            Log.e("Post Req Error:",e.toString());
            return 0;
        }
    }

    public  static int doPostRequest(URL url, JSONObject data){
        try {
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            // Set Timeout and method
            conn.setReadTimeout(7000);
            conn.setConnectTimeout(7000);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");
            conn.setDoOutput(true);
            conn.setDoInput(true);

//                conn.addRequestProperty("data",data.toString());
            OutputStream os = conn.getOutputStream();
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(data.toString());
            writer.flush();
            writer.close();
            os.close();
            conn.connect();
            return conn.getResponseCode();
        }
        catch (Exception e){
            Log.e("Post Req Error:",e.toString());
            return 0;
        }
    }
    public static void saveData(String s, SharedPreferences pref){
        try {
            JSONObject data = new JSONObject(s);
            String userId = data.getString("_id");
            SharedPreferences.Editor editor = pref.edit();
            editor.putBoolean("isLoggedin",true);
            editor.putString("User_ID", userId); // This will be used to map user id with Firebase token.
            editor.commit();
            Log.d("ResponseData",data.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    public static void sendRegistrationToServer(String refreshedToken, SharedPreferences sharedPref) {

        String user_id = sharedPref.getString("User_ID","NotFound");
        if(!user_id.equals("NotFound")){
            Log.d("Token",user_id+":"+refreshedToken);
            JSONObject data = new JSONObject();
            try {
                data.put(Constants.firebase_token,refreshedToken);
                URL tokenUpdateUrl = new URL(Constants.FIREBASE_TOEKN_UPDATE_URL+user_id);
                Log.d("Token_data",data.toString());
                HelperClass.doPostRequest(tokenUpdateUrl,data);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else{
            SharedPreferences.Editor editor = sharedPref.edit();
            editor.putString(Constants.firebase_token,refreshedToken);
            editor.commit();
        }
//        TODO: Call API to update users token
    }
}
