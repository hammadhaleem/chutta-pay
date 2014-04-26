package com.chuttapay.android;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

public class AsyncRequest extends AsyncTask<String, Void, String> {
	
	private Context context;
	
	private String URL;
	private String method;
	private JSONObject params;
	private OnTaskCompleted listener = null;
	private final static int NETWORK_STATUS_OK = 0;

	@Override
	protected void onPostExecute(String result) {
		super.onPostExecute(result);
		Log.d("result", result+"");
		if(listener != null && result != null){
			try {
				listener.onTaskCompleted(new JSONObject(result));
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}else if(result == null){
			Toast.makeText(context, "Failed to contact Server.", Toast.LENGTH_LONG).show();
		}
	}

	public AsyncRequest(Context context, String url, String method, JSONObject params, OnTaskCompleted listener){
		this.context = context;
		this.method = method;
		this.URL = url;
		this.params = params;
		this.listener = listener;
	}

/*	public AsyncRequest(Context context, String url, String method, String params){
		this.context = context;
		this.method = method;
		this.URL = url;
		this.params = params;
	}*/
	
	private int networkStatus(){
		int networkStatus = 1;
		ConnectivityManager connMgr = (ConnectivityManager) 
	        context.getSystemService(Context.CONNECTIVITY_SERVICE);
	    NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
	    if (networkInfo != null && networkInfo.isConnected()) 
		    networkStatus = 0;
		   return networkStatus;
	}

	@Override
	protected String doInBackground(String... urls) {
		HttpClient httpClient = new DefaultHttpClient();
		Log.d("inbgactivity", urls[0]);
		if(networkStatus() == NETWORK_STATUS_OK){
			if(method.equalsIgnoreCase("POST")){
				try{
					HttpPost request = new HttpPost(urls[0]);
					Log.d("asd", this.params.toString());
//					StringEntity parameters = new StringEntity(params);
					List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
	                Iterator<?> iter = this.params.keys();
	                while(iter.hasNext()){
	                	String key = (String) iter.next();
	                	nameValuePairs.add(new BasicNameValuePair(key, this.params.getString(key)));
	                }
					/*nameValuePairs.add(new BasicNameValuePair("phone_no",
	                        this.params.getString("phone_no")));
	                nameValuePairs.add(new BasicNameValuePair("passwd",
	                        this.params.getString("passwd")));
	                */
					request.setEntity(new UrlEncodedFormEntity(nameValuePairs));

	                HttpResponse response = httpClient.execute(request);
			        return EntityUtils.toString(response.getEntity());
				}
				catch(Exception e){
					e.printStackTrace();
					Log.d("bg exception", e.toString());
					return null;
				}
			}
			else if(method.equalsIgnoreCase("GET")){
				try{
					HttpGet request = new HttpGet(urls[0]);
					HttpResponse response = httpClient.execute(request);
			        return EntityUtils.toString(response.getEntity());
				}
				catch(Exception e){
					e.printStackTrace();
					Log.d("bg exception", e.toString());
					return null;
				}
			}
			
			else 
				return null;
		}
		else{
			return null;
		}
	}
}