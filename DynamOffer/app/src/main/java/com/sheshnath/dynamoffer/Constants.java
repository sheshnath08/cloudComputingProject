package com.sheshnath.dynamoffer;

import android.content.Context;

/**
 * Created by sheshnath on 11/13/2016.
 */

public class Constants {
    public static final String API_URL = "http://54.173.234.214:5000/api";
    public static final String SIGN_UP_URL = API_URL+"/users/register=True";
    public static final String LOGIN_URL=API_URL+"/users/login/userId=";
    public static final String USER_EMAIL="userEmail";
    public static final String USER_PASSWORD ="password";
    public static final String SIGNUP_ADDRESS="address";
    public static final String SIGNUP_NAME="name";
    public static final String SIGNUP_LOCATION="location";
    public static final String OFFER_URL=API_URL+"/offers/validity=now";
    public static final String USER_LOCATION_UPDATE_URL = API_URL+"/users/updateLocation=True"; // Send POST request
    public static final String OFFER_CLAIMS=API_URL+"/claims"; //send POST request with data. (offer_id, user_id)
    public static final String firebase_token = "firebaseToken";
    public static Context mainActivityContext;
    public static final String FIREBASE_TOEKN_UPDATE_URL = API_URL+"/users/updateTokenFor=";
    public static final String RECOMMENDED_OFFER_URL = API_URL+"/merchants/location/byMerchantLocation=spark?";
            //http://127.0.0.1:5000/api/merchants/location/byMerchantLocation=spark?lat=40.2454&lon=-40.45678&maxdist=5000&userId=58533df136e8b80e043b7e3d
//    # data = {'firebaseToken':'123544'}
//    # post("http://127.0.0.1:5000/api/users/updateTokenFor=8", json=data)
}
