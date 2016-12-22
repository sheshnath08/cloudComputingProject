package com.sheshnath.dynamoffer;

/**
 * Created by sheshnath on 11/17/2016.
 */

public class OfferModel {
    private String description;
    private String merchantName;
    private String offerID;

    public String getDescription() {
        return description;
    }

    public String getMerchantName() {
        return merchantName;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setMerchantName(String merchantName) {
        this.merchantName = merchantName;
    }
    public void setOfferID(String offerID){
        this.offerID = offerID;
    }
    public String getOfferID(){
        return this.offerID;
    }
}
