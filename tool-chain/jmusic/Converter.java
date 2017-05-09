import jm.music.data.*;
import jm.JMC;
import jm.util.*;
import java.io.File;

public final class Converter implements JMC {
  public static void main(String[] args) {
    if(args.length < 2) {
      System.out.println("USAGE: converter [input] [output]");
    } else {
      File file = new File(args[0]);
      Score s = new Score();
      if (args[0].endsWith(".mid")) {
	  Read.midi(s, args[0]);
	  System.out.println();
	  Write.xml(s, args[1]);
      }
      else if (args[0].endsWith(".xml")) {
	  Read.xml(s, args[0]);
	  System.out.println();
	  Write.midi(s, args[1]);
      }
    }
  }
}

