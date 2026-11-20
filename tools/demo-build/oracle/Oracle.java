import com.echo.domain.*; import com.echo.filter.*; import com.echo.service.*; import com.echo.logging.*;
import java.io.File; import java.util.*;
public class Oracle {
  static String q(String s){ return s==null?"null":"\""+s.replace("\\","\\\\").replace("\"","\\\"")+"\""; }
  public static void main(String[] a) throws Exception {
    RosterService rs=new RosterService(new ImportService(), new ExportService());
    List<String> ids=new ArrayList<>(); rs.getAvailableFeatures().forEach(f->ids.add(f.getFeatureId()));
    EnhancedRoster r=rs.createEnhancedRoster(new File(a[0]),new File(a[1]),ids);
    FilterManager fm=new FilterManager(); fm.createFiltersForRoster(r);
    StringBuilder b=new StringBuilder("{\n\"features\":[");
    StringJoiner j=new StringJoiner(","); rs.getAvailableFeatures().forEach(f->j.add(q(f.getFeatureName()))); b.append(j).append("],\n\"visible\":[");
    StringJoiner v=new StringJoiner(","); r.getOrderedVisibleHeaders().forEach(h->v.add(q(h))); b.append(v).append("],\n\"all\":[");
    StringJoiner h=new StringJoiner(","); r.getOrderedHeaders().forEach(x->h.add(q(x))); b.append(h).append("],\n\"campers\":[\n");
    StringJoiner cs=new StringJoiner(",\n");
    for(Camper c:r.getCampers()){ StringJoiner o=new StringJoiner(","); for(String x:r.getOrderedHeaders()) o.add(q(x)+":"+q(c.getValue(x))); cs.add("{"+o+"}"); }
    b.append(cs).append("\n],\n\"assertions\":[\n"); StringJoiner as=new StringJoiner(",\n");
    for(RosterFilter f:fm.getAllFilters()){ AssertionResult x=f.checkAssertion(r); as.add("{\"filter\":"+q(f.getFilterName())+",\"applicable\":"+x.applicable()+",\"failures\":"+x.failureCount()+",\"status\":"+q(x.statusText())+",\"claim\":"+q(x.claim())+"}"); }
    b.append(as).append("\n],\n\"report\":[\n"); StringJoiner rp=new StringJoiner(",\n");
    for(var row:ActivityReportData.compute(r)){ StringJoiner o=new StringJoiner(","); ActivityReportData.toCsvRow(row).forEach(s->o.add(q(s))); rp.add("["+o+"]"); }
    b.append(rp).append("\n],\n\"warnings\":[\n"); StringJoiner w=new StringJoiner(",\n");
    rs.getWarningManager().getWarningLog().forEach((t,l)->l.forEach(x->w.add("["+q(String.valueOf(t))+","+q(x.toString())+"]")));
    b.append(w).append("\n]\n}\n"); System.out.print(b);
  }
}
