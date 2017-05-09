import jm.music.data.*;
import jm.JMC;
import jm.util.*;
import java.io.File;

public final class Process implements JMC {
  public static void main(String[] args) {
    if(args.length < 2) {
      System.out.println("USAGE: process [input] [output]");
    } else {
      File file = new File(args[0]);
      Score s = new Score();
      Read.midi(s, args[0]);
      System.out.println();
      Write.xml(s, args[1]);
    }
  }
}
