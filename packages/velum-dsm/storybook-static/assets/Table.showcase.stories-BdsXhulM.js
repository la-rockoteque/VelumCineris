import{j as e,p as t,q as s,B as d}from"./iframe-v_xVpIIQ.js";import{S as p,a as c,b as r}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const y={title:"Components/Table"},m=[{name:"Magic Missile",level:1,status:"Ready"},{name:"Fireball",level:3,status:"Draft"},{name:"Teleport",level:7,status:"Published"}],n={render:()=>e.jsx(p,{maxWidth:"1080px",children:e.jsxs(c,{children:[e.jsx(r,{label:"Standard Rows",description:"Default striped dataset",minHeight:"260px",children:e.jsx(t,{children:e.jsx(s,{rows:m,onRowClick:()=>{},getRowActions:a=>[{key:"details",label:`Open ${a.name}`,icon:e.jsx("span",{children:"⌕"}),onClick:()=>{}},{key:"ai",label:`Run AI for ${a.name}`,icon:e.jsx("span",{children:"✦"}),onClick:()=>{}}],columns:[{key:"name",header:"Spell"},{key:"level",header:"Level",align:"center",width:"90px"},{key:"status",header:"Status",width:"140px",render:a=>e.jsx(d,{children:String(a.status)})}]})})}),e.jsx(r,{label:"Empty State",description:"No results available",minHeight:"260px",children:e.jsx(t,{children:e.jsx(s,{rows:[],onRowClick:()=>{},emptyMessage:"No matching entries.",columns:[{key:"name",header:"Name"},{key:"type",header:"Type"}]})})})]})})};var l,i,o;n.parameters={...n.parameters,docs:{...(l=n.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Standard Rows" description="Default striped dataset" minHeight="260px">
          <TableWrap>
            <Table rows={spellRows} onRowClick={() => undefined} getRowActions={row => [{
            key: "details",
            label: \`Open \${row.name}\`,
            icon: <span>⌕</span>,
            onClick: () => undefined
          }, {
            key: "ai",
            label: \`Run AI for \${row.name}\`,
            icon: <span>✦</span>,
            onClick: () => undefined
          }]} columns={[{
            key: "name",
            header: "Spell"
          }, {
            key: "level",
            header: "Level",
            align: "center",
            width: "90px"
          }, {
            key: "status",
            header: "Status",
            width: "140px",
            render: row => <Badge>{String(row.status)}</Badge>
          }]} />
          </TableWrap>
        </StateCase>
        <StateCase label="Empty State" description="No results available" minHeight="260px">
          <TableWrap>
            <Table rows={[]} onRowClick={() => undefined} emptyMessage="No matching entries." columns={[{
            key: "name",
            header: "Name"
          }, {
            key: "type",
            header: "Type"
          }]} />
          </TableWrap>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(o=(i=n.parameters)==null?void 0:i.docs)==null?void 0:o.source}}};const S=["Showcase"];export{n as Showcase,S as __namedExportsOrder,y as default};
