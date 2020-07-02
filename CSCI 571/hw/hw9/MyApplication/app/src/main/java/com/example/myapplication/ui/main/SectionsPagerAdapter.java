package com.example.myapplication.ui.main;

import android.content.Context;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

import com.example.myapplication.R;
import com.example.myapplication.Tab1;
import com.example.myapplication.Tab2;
import com.example.myapplication.Tab3;

import org.json.JSONObject;

/**
 * A [FragmentPagerAdapter] that returns a fragment corresponding to
 * one of the sections/tabs/pages.
 */
public class SectionsPagerAdapter extends FragmentPagerAdapter {

    @StringRes
    private static final int[] TAB_TITLES = new int[]{R.string.tab_text_1, R.string.tab_text_2,R.string.tab_text_3};
    private final Context mContext;
    private final JSONObject mjsonObject;
    private final Bundle mbundle;

    public SectionsPagerAdapter(Context context, FragmentManager fm, JSONObject jsonObject, Bundle bundle) {
        super(fm);
        mContext = context;
        mjsonObject = jsonObject;
        mbundle  = bundle;
    }

    @Override
    public Fragment getItem(int position) {
        // getItem is called to instantiate the fragment for the given page.
        // Return a PlaceholderFragment (defined as a static inner class below).

        switch(position){
            case 0:
                Tab1 tab1 = new Tab1(mjsonObject, mbundle);
                return tab1;
            case 1:
                Tab2 tab2 = new Tab2(mjsonObject);
                return tab2;
            case 2:
                Tab3 tab3 = new Tab3(mjsonObject, mbundle);
                return tab3;
            default:
                return null;
        }
//        return PlaceholderFragment.newInstance(position + 1);
    }


    @Nullable
    @Override
    public CharSequence getPageTitle(int position) {
        return mContext.getResources().getString(TAB_TITLES[position]);
    }

    @Override
    public int getCount() {
        // Show 3 total pages.
        return 3;
    }
}