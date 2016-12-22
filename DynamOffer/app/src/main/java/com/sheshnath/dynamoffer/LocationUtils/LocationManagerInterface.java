package com.sheshnath.dynamoffer.LocationUtils;

import android.location.Location;

/**
 * Created by sheshnath on 12/6/2016.
 */
public interface LocationManagerInterface {
    String TAG = LocationManagerInterface.class.getSimpleName();
    void locationFetched(Location mLocation, Location oldLocation, String time, String locationProvider);
}

