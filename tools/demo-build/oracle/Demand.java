import com.echo.domain.*; import com.echo.service.*; import java.io.File; import java.util.*;
public class Demand { public static void main(String[] a) throws Exception {
 RosterService rs=new RosterService(new ImportService(), new ExportService()); List<String> ids=new ArrayList<>(); rs.getAvailableFeatures().forEach(f->ids.add(f.getFeatureId()));
 EnhancedRoster r=rs.createEnhancedRoster(new File(a[0]),new File(a[1]),ids); List<Camper> c=new ArrayList<>(r.getCampers()); c.sort(DemandSort.comparator(a[2]));
 for(Camper x:c) System.out.println(x.getValue("Last Name")+" "+DemandSort.rankFor(x,a[2])); }}
