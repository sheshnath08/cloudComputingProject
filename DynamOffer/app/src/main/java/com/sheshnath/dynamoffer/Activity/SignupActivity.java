package com.sheshnath.dynamoffer.Activity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.sheshnath.dynamoffer.Constants;
import com.sheshnath.dynamoffer.HelperClass;
import com.sheshnath.dynamoffer.R;

import org.json.JSONObject;

import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

/**
 * Created by sheshnath on 11/2/2016.
 */

public class SignupActivity  extends AppCompatActivity {
    private AutoCompleteTextView mUserIdView;
    private EditText mPasswordView;
    private AutoCompleteTextView mNameView;
    private EditText mAddressView;
    private SignupTask mSignUpTask = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        mUserIdView = (AutoCompleteTextView) findViewById(R.id.signup_email_view);
        mNameView = (AutoCompleteTextView) findViewById(R.id.signup_name_textview);
        mPasswordView = (EditText) findViewById(R.id.signup_password);
        mAddressView = (EditText) findViewById(R.id.signup_adddress);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);

        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
                Intent intent = new Intent(getBaseContext(),LoginActivity.class);
                startActivity(intent);
            }
        });

        Button mRegister = (Button) findViewById(R.id.sign_up_button);
        mRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptSignUp();
            }
        });
        // Set up the Registration form.
    }

    private void attemptSignUp() {
        String userId = mUserIdView.getText().toString();
        String password = mPasswordView.getText().toString();
        String address = mAddressView.getText().toString();
        String name = mNameView.getText().toString();
        mSignUpTask = new SignupTask(userId,name,password,address);
        mSignUpTask.execute((Void)null);
    }

    public class SignupTask extends AsyncTask<Void,Void, Boolean> {
        private final String mEmail;
        private final String mPassword;
        private final String mName;
        private final String mAddress;
        private final String mFirebaseToken;

        public SignupTask(String email, String name, String password, String address){
            mEmail = email;
            mPassword = password;
            mAddress = address;
            mName = name;
            SharedPreferences sharedPref = getSharedPreferences(
                    getString(R.string.preference_file_key), Context.MODE_PRIVATE);
            mFirebaseToken = sharedPref.getString(getString(R.string.firebaseToken),"null");
        }
        @Override
        protected Boolean doInBackground(Void... params) {
            //TODO: Attemp to call API to register the user.
            try {
                URL url = new URL(Constants.SIGN_UP_URL);
                JSONObject postDataParams = new JSONObject();
                postDataParams.put(Constants.USER_EMAIL,mEmail);
                postDataParams.put(Constants.USER_PASSWORD,mPassword);
                postDataParams.put(Constants.SIGNUP_ADDRESS,mAddress);
                postDataParams.put(Constants.SIGNUP_NAME,mName);

                postDataParams.put(getString(R.string.firebaseToken),mFirebaseToken);
                postDataParams.put("lat",34.4);
                postDataParams.put("lon",34.4);
//                postDataParams.put(Constants.SIGNUP_LOCATION,location);
                Log.e("SignupParams: ",postDataParams.toString());
                SharedPreferences sharedPref = getSharedPreferences(
                        getString(R.string.preference_file_key),Context.MODE_PRIVATE);
                int responseCode= HelperClass.dosignupPostRequest(url,postDataParams,sharedPref);
                Log.i("SignUP_ ResponseCode",responseCode+"");
                if (responseCode == HttpsURLConnection.HTTP_OK) {
                    return true;
                }
                else {
                    return false;
                }
            }
            catch (Exception e){
                Log.e("Login Error:",e.toString());
            }
            return null;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
//            super.onPostExecute(success);
            if(success){
//                TODO: Show home page or setting page here and finish signUp Activity
                finish();
                SharedPreferences sharedPref = getSharedPreferences(
                        getString(R.string.preference_file_key), Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPref.edit();
                editor.putBoolean(getString(R.string.is_logged_in),true);
                editor.putString("name",mName);
                editor.commit();
                startMainAcitivity();
            }
            else{
                mUserIdView.setError(getString(R.string.error_incorrect_password));
            }
        }
    }
    private void startMainAcitivity() {
        Intent intent = new Intent(this,MainActivity.class);
        startActivity(intent);
    }

}
