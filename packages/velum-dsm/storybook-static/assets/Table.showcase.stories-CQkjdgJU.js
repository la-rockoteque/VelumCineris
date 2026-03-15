import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{i as t,j as s,B as d}from"./VelumProvider-Cnx-m3OC.js";import{S as p,a as m,b as r}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const b={title:"Components/Table"},c=[{name:"Magic Missile",level:1,status:"Ready"},{name:"Fireball",level:3,status:"Draft"},{name:"Teleport",level:7,status:"Published"}],a={render:()=>e.jsx(p,{maxWidth:"1080px",children:e.jsxs(m,{children:[e.jsx(r,{label:"Standard Rows",description:"Default striped dataset",minHeight:"260px",children:e.jsx(t,{children:e.jsx(s,{rows:c,columns:[{key:"name",header:"Spell"},{key:"level",header:"Level",align:"center",width:"90px"},{key:"status",header:"Status",width:"140px",render:o=>e.jsx(d,{children:String(o.status)})}]})})}),e.jsx(r,{label:"Empty State",description:"No results available",minHeight:"260px",children:e.jsx(t,{children:e.jsx(s,{rows:[],emptyMessage:"No matching entries.",columns:[{key:"name",header:"Name"},{key:"type",header:"Type"}]})})})]})})};var n,l,i;a.parameters={...a.parameters,docs:{...(n=a.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Standard Rows" description="Default striped dataset" minHeight="260px">
          <TableWrap>
            <Table rows={spellRows} columns={[{
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
            <Table rows={[]} emptyMessage="No matching entries." columns={[{
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
}`,...(i=(l=a.parameters)==null?void 0:l.docs)==null?void 0:i.source}}};const g=["Showcase"];export{a as Showcase,g as __namedExportsOrder,b as default};
