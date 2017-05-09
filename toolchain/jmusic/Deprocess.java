import jm.music.data.*;
import jm.JMC;
import jm.util.*;
import java.io.File;

public final class Deprocess implements JMC {
  public static void main(String[] args) {
    if(args.length < 2) {
      System.out.println("USAGE: deprocess [input] [output]");
    } else {
      File file = new File(args[0]);
      Score s = new Score();
      Read.xml(s, args[0]);
      System.out.println();
      Write.midi(s, args[1]);
    }
  }
}
