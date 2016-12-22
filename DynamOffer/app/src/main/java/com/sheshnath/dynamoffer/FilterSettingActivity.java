package com.sheshnath.dynamoffer;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;


/**
 * Created by sheshnath on 11/9/2016.
 */

public class FilterSettingActivity extends AppCompatActivity {
    private TextView mSaveSettings;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.filter_setting_view);
        mSaveSettings = (TextView)findViewById(R.id.save_settings_button);
        mSaveSettings.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}
