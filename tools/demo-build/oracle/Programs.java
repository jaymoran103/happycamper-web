import com.echo.domain.*; import com.echo.feature.*; import com.echo.service.*;
import java.io.File; import java.util.*;
public class Programs { public static void main(String[] a) throws Exception {
 RosterService rs=new RosterService(new ImportService(), new ExportService());
 List<String> ids=new ArrayList<>(); rs.getAvailableFeatures().forEach(f->ids.add(f.getFeatureId()));
 EnhancedRoster r=rs.createEnhancedRoster(new File(a[0]),new File(a[1]),ids);
 Map<String,TreeMap<String,Integer>> m=new TreeMap<>();
 for(Camper c:r.getCampers()){String p=c.getValue("Program"); if(p==null||p.isEmpty())p="(none)"; m.computeIfAbsent(p,k->new TreeMap<>()).merge(c.getValue("Rounds Assigned"),1,Integer::sum);}
 Map<Integer,List<String>> g=ProgramFeature.getProgramsByRoundCount(r); Map<String,Integer> bucket=new HashMap<>(); g.forEach((k,v)->v.forEach(p->bucket.put(p,k)));
 StringJoiner j=new StringJoiner(",\n"); m.forEach((p,t)->{StringJoiner x=new StringJoiner(","); t.forEach((k,v)->x.add("\""+k+"\":"+v)); j.add("{\"name\":\""+p+"\",\"group\":"+bucket.get(p)+",\"counts\":{"+x+"}}");});
 System.out.println("["+j+"]"); System.err.println("campers="+r.getCampers().size());
}}
