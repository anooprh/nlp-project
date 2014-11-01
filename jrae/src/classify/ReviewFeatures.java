package classify;

import java.util.*;

import org.jblas.DoubleMatrix;

public class ReviewFeatures implements LabeledDatum<Double,Integer>{
	private String ReviewStr;
	private List<Double> Features;
	private int Label, Index;
	public DoubleMatrix x;
	public ReviewFeatures(String review, int label, int itemNo)
	{
		this.Label = label;
		this.ReviewStr = review;
		this.Index = itemNo;
	}
	public ReviewFeatures(String review, int label, int itemNo, double[] features, DoubleMatrix x){
		this(review, label, itemNo, features);
		this.x = x;
	}

	public ReviewFeatures(String review, int label, int itemNo, double[] features)
	{
		this(review,label,itemNo);
		this.Features = new ArrayList<Double>( features.length );
		for(double feature : features)
	    	this.Features.add(feature);
	}
	
	@Override
	public Collection<Double> getFeatures() 
	{
		return Features;
	}

	@Override
	public Integer getLabel() 
	{
		return Label;
	}
	
	@Override
	public String toString()
	{
		return Index + " // " + ReviewStr;
	}
	
	public int getIndex()
	{
		return Index;
	}
	
}
