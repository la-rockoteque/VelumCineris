import{j as e,p as s}from"./iframe-v_xVpIIQ.js";import{S as l,a as i,b as p}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const x={title:"Components/Layout/TableWrap"},t={render:()=>e.jsx(l,{maxWidth:"1100px",children:e.jsx(i,{columns:"1fr",children:e.jsx(p,{label:"Wide Data Table",description:"Horizontal overflow preserved for larger tables",minHeight:"260px",children:e.jsx(s,{children:e.jsxs("table",{style:{width:"100%",minWidth:"760px",borderCollapse:"collapse"},children:[e.jsx("thead",{children:e.jsx("tr",{children:["Source","Sheet","Rows","Updated","Owner","Status"].map(a=>e.jsx("th",{style:{textAlign:"left",padding:"12px"},children:a},a))})}),e.jsx("tbody",{children:[["Modern","Lexicon","312","Today","Rocko","Healthy"],["Fantasy","Bestiary","128","Yesterday","Rocko","Pending"],["Shared","Timeline","42","Today","Team","Healthy"]].map(a=>e.jsx("tr",{children:a.map(r=>e.jsx("td",{style:{padding:"12px"},children:r},r))},a.join("-")))})]})})})})})};var n,o,d;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr">
        <StateCase label="Wide Data Table" description="Horizontal overflow preserved for larger tables" minHeight="260px">
          <TableWrap>
            <table style={{
            width: "100%",
            minWidth: "760px",
            borderCollapse: "collapse"
          }}>
              <thead>
                <tr>
                  {["Source", "Sheet", "Rows", "Updated", "Owner", "Status"].map(heading => <th key={heading} style={{
                  textAlign: "left",
                  padding: "12px"
                }}>
                      {heading}
                    </th>)}
                </tr>
              </thead>
              <tbody>
                {[["Modern", "Lexicon", "312", "Today", "Rocko", "Healthy"], ["Fantasy", "Bestiary", "128", "Yesterday", "Rocko", "Pending"], ["Shared", "Timeline", "42", "Today", "Team", "Healthy"]].map(row => <tr key={row.join("-")}>
                    {row.map(cell => <td key={cell} style={{
                  padding: "12px"
                }}>
                        {cell}
                      </td>)}
                  </tr>)}
              </tbody>
            </table>
          </TableWrap>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(d=(o=t.parameters)==null?void 0:o.docs)==null?void 0:d.source}}};const y=["Showcase"];export{t as Showcase,y as __namedExportsOrder,x as default};
