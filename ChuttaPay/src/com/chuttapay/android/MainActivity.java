package com.chuttapay.android;


import android.support.v7.app.ActionBarActivity;
import android.content.SharedPreferences;
import android.os.Bundle;

public class MainActivity extends ActionBarActivity {

	private static String user_id = null;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        SharedPreferences settings = getApplicationContext().getSharedPreferences("user_id", 0);
        user_id = settings.getString("user_id", null);
        
		if (savedInstanceState == null) {
			if(user_id == null){
				getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new RegistrationFragment())
                    .commit();
			}
			else{
				getSupportFragmentManager().beginTransaction()
                .add(R.id.container, new PaymentFragment())
                .commit();
			}
        
		}
    }
}
