package Reader;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

public class Reader {
	public static void main(String[] args) throws FileNotFoundException, ParseException{
		File file = new File("userid-timestamp-artid-artname-traid-traname.tsv");
		PrintWriter writer = new PrintWriter(new File("newfile.data"));
		
		//System.out.println(file.exists());
		Scanner reader = new Scanner(file);
		
		int i = 0;
		while(reader.hasNext()){
			String string = reader.nextLine();
			String newString = formatString(string);
			
			writer.println(newString);
			System.out.println("current line:" + i);
			i += 1;
		}
		
		writer.close();
		reader.close();
	}

	private static String formatString(String string) throws ParseException {
		String[] array = string.split("\t");
		
		int userID = Integer.valueOf(array[0].indexOf("_")+1);
				
		String date = array[1].substring(0, array[1].indexOf('T'))+" "+array[1].substring(array[1].indexOf('T')+1, array[1].length()-1);
		SimpleDateFormat format = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss");
		Date time = format.parse(date);
		
		//System.out.println(time.getTime());
		String newString = userID + "\t";
		newString += time.getTime() + "\t";
		newString += array[array.length-2];
		
		return newString;
	}
}
