/***************************************************************************
 *   Copyright (c) 2015 Stefan Tröger <stefantroeger@gmx.net>              *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/


#include "PreCompiled.h"

#ifndef _PreComp_
# include <Python.h>
# include <vtkFieldData.h>
# include <vtkPointData.h>
#endif

#include "FemPostFilter.h"
#include "FemPostPipeline.h"
#include <Base/Console.h>
#include <App/Document.h>
#include <App/DocumentObjectPy.h>


#include <vtkFieldData.h>
#include <vtkPointData.h>
#include <vtkMath.h>

using namespace Fem;
using namespace App;

PROPERTY_SOURCE(Fem::FemPostFilter, Fem::FemPostObject)


FemPostFilter::FemPostFilter()
{
    ADD_PROPERTY(Input,(0));
}

FemPostFilter::~FemPostFilter()
{

}

void FemPostFilter::addFilterPipeline(const FemPostFilter::FilterPipeline& p, std::string name) {
    m_pipelines[name] = p;
}

FemPostFilter::FilterPipeline& FemPostFilter::getFilterPipeline(std::string name) {
    return m_pipelines[name];
}

void FemPostFilter::setActiveFilterPipeline(std::string name) {

    if(m_activePipeline != name && isValid()) {
        m_activePipeline = name;
    }
}

DocumentObjectExecReturn* FemPostFilter::execute(void) {

    if(!m_pipelines.empty() && !m_activePipeline.empty()) {
        FemPostFilter::FilterPipeline& pipe = m_pipelines[m_activePipeline];
        if (m_activePipeline.length() >= 11) {
            std::string LineClip = m_activePipeline.substr(0,13);
            std::string PointClip = m_activePipeline.substr(0,11);
            if ((LineClip == "DataAlongLine") || (PointClip == "DataAtPoint")) {
                pipe.filterSource->SetSourceData(getInputData());
                pipe.filterTarget->Update();

                Data.setValue(pipe.filterTarget->GetOutputDataObject(0));
            }
        } else {
            pipe.source->SetInputDataObject(getInputData());
            pipe.target->Update();
            Data.setValue(pipe.target->GetOutputDataObject(0));
        }

    }
    return StdReturn;
}

vtkDataObject* FemPostFilter::getInputData() {

    if(Input.getValue()) {
        return Input.getValue<FemPostObject*>()->Data.getValue();
    }
    else {
        //get the pipeline and use the pipelinedata
        std::vector<App::DocumentObject*> objs = getDocument()->getObjectsOfType(FemPostPipeline::getClassTypeId());
        for(std::vector<App::DocumentObject*>::iterator it = objs.begin(); it != objs.end(); ++it) {

            if(static_cast<FemPostPipeline*>(*it)->holdsPostObject(this)) {

                return static_cast<FemPostObject*>(*it)->Data.getValue();
            }
        }
    }

    return NULL;
}


PROPERTY_SOURCE(Fem::FemPostClipFilter, Fem::FemPostFilter)

FemPostClipFilter::FemPostClipFilter(void) : FemPostFilter() {

    ADD_PROPERTY_TYPE(Function, (0), "Clip", App::Prop_None, "The function object which defines the clip regions");
    ADD_PROPERTY_TYPE(InsideOut, (false), "Clip", App::Prop_None, "Invert the clip direction");
    ADD_PROPERTY_TYPE(CutCells, (false), "Clip", App::Prop_None, "Decides if cells are cuttet and interpolated or if the cells are kept as a whole");

    FilterPipeline clip;
    m_clipper           = vtkSmartPointer<vtkTableBasedClipDataSet>::New();
    clip.source         = m_clipper;
    clip.target         = m_clipper;
    addFilterPipeline(clip, "clip");

    FilterPipeline extr;
    m_extractor         = vtkSmartPointer<vtkExtractGeometry>::New();
    extr.source         = m_extractor;
    extr.target         = m_extractor;
    addFilterPipeline(extr, "extract");

    m_extractor->SetExtractInside(0);
    setActiveFilterPipeline("extract");
}

FemPostClipFilter::~FemPostClipFilter() {

}

void FemPostClipFilter::onChanged(const Property* prop) {

    if(prop == &Function) {

        if(Function.getValue() && Function.getValue()->isDerivedFrom(FemPostFunction::getClassTypeId())) {
            m_clipper->SetClipFunction(static_cast<FemPostFunction*>(Function.getValue())->getImplicitFunction());
            m_extractor->SetImplicitFunction(static_cast<FemPostFunction*>(Function.getValue())->getImplicitFunction());
        }
    }
    else if(prop == &InsideOut) {

        m_clipper->SetInsideOut(InsideOut.getValue());
        m_extractor->SetExtractInside( (InsideOut.getValue()) ? 1 : 0 );
    }
    else if(prop == &CutCells) {

        if(!CutCells.getValue())
            setActiveFilterPipeline("extract");
        else
            setActiveFilterPipeline("clip");
    };

    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostClipFilter::mustExecute(void) const {

    if(Function.isTouched() ||
       InsideOut.isTouched() ||
       CutCells.isTouched()) {

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

DocumentObjectExecReturn* FemPostClipFilter::execute(void) {

    if(!m_extractor->GetImplicitFunction())
        return StdReturn;

    return Fem::FemPostFilter::execute();
}

PROPERTY_SOURCE(Fem::FemPostDataAlongLineFilter, Fem::FemPostFilter)

FemPostDataAlongLineFilter::FemPostDataAlongLineFilter(void) : FemPostFilter() {

    ADD_PROPERTY_TYPE(Point1,(Base::Vector3d(0.0,0.0,0.0)), "DataAlongLine", App::Prop_None, "The point 1 used to define end point of line");
    ADD_PROPERTY_TYPE(Point2,(Base::Vector3d(0.0,0.0,1.0)), "DataAlongLine", App::Prop_None, "The point 2 used to define end point of line");
    ADD_PROPERTY_TYPE(Resolution,(100), "DataAlongLine", App::Prop_None, "The number of intervals between the 2 end points of line");
    ADD_PROPERTY_TYPE(XAxisData,(0), "DataAlongLine",App::Prop_None,"X axis data values used for plotting");
    ADD_PROPERTY_TYPE(YAxisData,(0), "DataAlongLine",App::Prop_None,"Y axis data values used for plotting");
    ADD_PROPERTY_TYPE(PlotData ,(""),"DataAlongLine",App::Prop_None,"Field used for plotting");

    PlotData.setStatus(App::Property::ReadOnly, true);
    XAxisData.setStatus(App::Property::ReadOnly, true);
    YAxisData.setStatus(App::Property::ReadOnly, true);

    FilterPipeline clip;

    m_line = vtkSmartPointer<vtkLineSource>::New();
    const Base::Vector3d& vec1 = Point1.getValue();
    m_line->SetPoint1(vec1.x, vec1.y, vec1.z);
    const Base::Vector3d& vec2 = Point2.getValue();
    m_line->SetPoint2(vec2.x, vec2.y, vec2.z);
    m_line->SetResolution(Resolution.getValue());


    m_probe = vtkSmartPointer<vtkProbeFilter>::New();
    m_probe->SetInputConnection(m_line->GetOutputPort());
    m_probe->SetValidPointMaskArrayName("ValidPointArray");
    m_probe->SetPassPointArrays(1);
    m_probe->SetPassCellArrays(1);
    // needs vtk > 6.1
#if (VTK_MAJOR_VERSION > 6) || (VTK_MINOR_VERSION > 1)
    m_probe->ComputeToleranceOff();
    m_probe->SetTolerance(0.01);
#endif

    clip.filterSource   = m_probe;
    clip.filterTarget   = m_probe;

    addFilterPipeline(clip, "DataAlongLine");
    setActiveFilterPipeline("DataAlongLine");
}

FemPostDataAlongLineFilter::~FemPostDataAlongLineFilter() {

}

DocumentObjectExecReturn* FemPostDataAlongLineFilter::execute(void) {

    //recalculate the filter
    return Fem::FemPostFilter::execute();
}


void FemPostDataAlongLineFilter::onChanged(const Property* prop) {
    if(prop == &Point1) {
        const Base::Vector3d& vec1 = Point1.getValue();
        m_line->SetPoint1(vec1.x, vec1.y, vec1.z);
    }
    else if(prop == &Point2) {
        const Base::Vector3d& vec2 = Point2.getValue();
        m_line->SetPoint2(vec2.x, vec2.y, vec2.z);
    }
    else if(prop == &Resolution) {
        m_line->SetResolution(Resolution.getValue());
    }
    else if(prop == &PlotData) {
        GetAxisData();
    }
    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostDataAlongLineFilter::mustExecute(void) const {

    if(Point1.isTouched() ||
       Point2.isTouched() ||
       Resolution.isTouched()){

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

void FemPostDataAlongLineFilter::GetAxisData() {

    std::vector<double> coords;
    std::vector<double> values;

    vtkSmartPointer<vtkDataObject> data = m_probe->GetOutputDataObject(0);
    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);
    vtkDataArray* pdata = dset->GetPointData()->GetArray(PlotData.getValue());
    vtkDataArray *tcoords = dset->GetPointData()->GetTCoords("Texture Coordinates");

    int component = 0;

    const Base::Vector3d& vec1 = Point1.getValue();
    const Base::Vector3d& vec2 = Point2.getValue();
    const Base::Vector3d diff = vec1 - vec2;
    double Len = diff.Length();

    for(int i=0; i<dset->GetNumberOfPoints(); ++i) {

        double value = 0;
        if(pdata->GetNumberOfComponents() == 1)
            value = pdata->GetComponent(i, component);
        else {
            for(int j=0; j<pdata->GetNumberOfComponents(); ++j)
                value += std::pow(pdata->GetComponent(i, j),2);

            value = std::sqrt(value);
        }
        values.push_back(value);
        double tcoord = tcoords->GetComponent(i, component);
        coords.push_back(tcoord*Len);
    }
    YAxisData.setValues(values);
    XAxisData.setValues(coords);
}

PROPERTY_SOURCE(Fem::FemPostDataAtPointFilter, Fem::FemPostFilter)

FemPostDataAtPointFilter::FemPostDataAtPointFilter(void) : FemPostFilter() {

    ADD_PROPERTY_TYPE(Center,(Base::Vector3d(0.0,0.0,1.0)), "DataAtPoint", App::Prop_None, "The center used to define the center of the point");
    ADD_PROPERTY_TYPE(Radius,(0), "DataAtPoint", App::Prop_None, "The point 2 used to define end point of line");
    ADD_PROPERTY_TYPE(PointData,(0), "DataAtPoint",App::Prop_None,"Point data values used for plotting");
    ADD_PROPERTY_TYPE(FieldName,(""),"DataAtPoint",App::Prop_None,"Field used for plotting");
    ADD_PROPERTY_TYPE(Unit,(""),"DataAtPoint",App::Prop_None,"Unit used for Field");

    PointData.setStatus(App::Property::ReadOnly, true);
    FieldName.setStatus(App::Property::ReadOnly, true);
    Unit.setStatus(App::Property::ReadOnly, true);

    FilterPipeline clip;

    m_point = vtkSmartPointer<vtkPointSource>::New();
    const Base::Vector3d& vec = Center.getValue();
    m_point->SetCenter(vec.x, vec.y, vec.z);
    m_point->SetRadius(0);

    m_probe = vtkSmartPointer<vtkProbeFilter>::New();
    m_probe->SetInputConnection(m_point->GetOutputPort());
    m_probe->SetValidPointMaskArrayName("ValidPointArray");
    m_probe->SetPassPointArrays(1);
    m_probe->SetPassCellArrays(1);
    // needs vtk > 6.1
#if (VTK_MAJOR_VERSION > 6) || (VTK_MINOR_VERSION > 1)
    m_probe->ComputeToleranceOff();
    m_probe->SetTolerance(0.01);
#endif

    clip.filterSource   = m_probe;
    clip.filterTarget   = m_probe;

    addFilterPipeline(clip, "DataAtPoint");
    setActiveFilterPipeline("DataAtPoint");
}

FemPostDataAtPointFilter::~FemPostDataAtPointFilter() {

}

DocumentObjectExecReturn* FemPostDataAtPointFilter::execute(void) {

    //recalculate the filter
    return Fem::FemPostFilter::execute();
}


void FemPostDataAtPointFilter::onChanged(const Property* prop) {
    if(prop == &Center) {
        const Base::Vector3d& vec = Center.getValue();
        m_point->SetCenter(vec.x, vec.y, vec.z);
    }
    else if(prop == &FieldName) {
        GetPointData();
    }
    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostDataAtPointFilter::mustExecute(void) const {

    if(Center.isTouched()){

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

void FemPostDataAtPointFilter::GetPointData() {

    std::vector<double> values;

    vtkSmartPointer<vtkDataObject> data = m_probe->GetOutputDataObject(0);
    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);
    vtkDataArray* pdata = dset->GetPointData()->GetArray(FieldName.getValue());

    int component = 0;

    for(int i=0; i<dset->GetNumberOfPoints(); ++i) {

        double value = 0;
        if(pdata->GetNumberOfComponents() == 1)
            value = pdata->GetComponent(i, component);
        else {
            for(int j=0; j<pdata->GetNumberOfComponents(); ++j)
                value += std::pow(pdata->GetComponent(i, j),2);

            value = std::sqrt(value);
        }
        values.push_back(value);
    }
    PointData.setValues(values);
}

PROPERTY_SOURCE(Fem::FemPostScalarClipFilter, Fem::FemPostFilter)

FemPostScalarClipFilter::FemPostScalarClipFilter(void) : FemPostFilter() {

    ADD_PROPERTY_TYPE(Value, (0), "Clip", App::Prop_None, "The scalar value used to clip the selected field");
    ADD_PROPERTY_TYPE(Scalars, (long(0)), "Clip", App::Prop_None, "The field used to clip");
    ADD_PROPERTY_TYPE(InsideOut, (false), "Clip", App::Prop_None, "Invert the clip direction");

    Value.setConstraints(&m_constraints);

    FilterPipeline clip;
    m_clipper           = vtkSmartPointer<vtkTableBasedClipDataSet>::New();
    clip.source         = m_clipper;
    clip.target         = m_clipper;
    addFilterPipeline(clip, "clip");
    setActiveFilterPipeline("clip");
}

FemPostScalarClipFilter::~FemPostScalarClipFilter() {

}

DocumentObjectExecReturn* FemPostScalarClipFilter::execute(void) {

    std::string val;
    if(m_scalarFields.getEnums() && Scalars.getValue() >= 0)
        val = Scalars.getValueAsString();

    std::vector<std::string> array;

    vtkSmartPointer<vtkDataObject> data = getInputData();
    if(!data || !data->IsA("vtkDataSet"))
        return StdReturn;

    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);
    vtkPointData* pd = dset->GetPointData();

    for(int i=0; i<pd->GetNumberOfArrays(); ++i) {
        if(pd->GetArray(i)->GetNumberOfComponents()==1)
            array.push_back(pd->GetArrayName(i));
    }

    App::Enumeration empty;
    Scalars.setValue(empty);
    m_scalarFields.setEnums(array);
    Scalars.setValue(m_scalarFields);

    std::vector<std::string>::iterator it = std::find(array.begin(), array.end(), val);
    if(!val.empty() && it != array.end())
        Scalars.setValue(val.c_str());

    //recalculate the filter
    return Fem::FemPostFilter::execute();
}


void FemPostScalarClipFilter::onChanged(const Property* prop) {

    if(prop == &Value) {
        m_clipper->SetValue(Value.getValue());
    }
    else if(prop == &InsideOut) {
        m_clipper->SetInsideOut(InsideOut.getValue());
    }
    else if(prop == &Scalars && (Scalars.getValue() >= 0)) {
        m_clipper->SetInputArrayToProcess(0, 0, 0,
                                          vtkDataObject::FIELD_ASSOCIATION_POINTS, Scalars.getValueAsString() );
        setConstraintForField();
    }

    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostScalarClipFilter::mustExecute(void) const {

    if(Value.isTouched() ||
       InsideOut.isTouched() ||
       Scalars.isTouched()) {

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

void FemPostScalarClipFilter::setConstraintForField() {

    vtkSmartPointer<vtkDataObject> data = getInputData();
    if(!data || !data->IsA("vtkDataSet"))
        return;

    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);

    vtkDataArray* pdata = dset->GetPointData()->GetArray(Scalars.getValueAsString());
    double p[2];
    pdata->GetRange(p);
    m_constraints.LowerBound = p[0];
    m_constraints.UpperBound = p[1];
    m_constraints.StepSize = (p[1]-p[0])/100.;
}


PROPERTY_SOURCE(Fem::FemPostWarpVectorFilter, Fem::FemPostFilter)

FemPostWarpVectorFilter::FemPostWarpVectorFilter(void): FemPostFilter() {

    ADD_PROPERTY_TYPE(Factor, (0), "Warp", App::Prop_None, "The factor by which the vector is added to the node positions");
    ADD_PROPERTY_TYPE(Vector, (long(0)), "Warp", App::Prop_None, "The field added to the node position");

    FilterPipeline warp;
    m_warp              = vtkSmartPointer<vtkWarpVector>::New();
    warp.source         = m_warp;
    warp.target         = m_warp;
    addFilterPipeline(warp, "warp");
    setActiveFilterPipeline("warp");
}

FemPostWarpVectorFilter::~FemPostWarpVectorFilter() {

}


DocumentObjectExecReturn* FemPostWarpVectorFilter::execute(void) {

    std::string val;
    if(m_vectorFields.getEnums() && Vector.getValue() >= 0)
        val = Vector.getValueAsString();

    std::vector<std::string> array;

    vtkSmartPointer<vtkDataObject> data = getInputData();
    if(!data || !data->IsA("vtkDataSet"))
        return StdReturn;

    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);
    vtkPointData* pd = dset->GetPointData();

    for(int i=0; i<pd->GetNumberOfArrays(); ++i) {
        if(pd->GetArray(i)->GetNumberOfComponents()==3)
            array.push_back(pd->GetArrayName(i));
    }

    App::Enumeration empty;
    Vector.setValue(empty);
    m_vectorFields.setEnums(array);
    Vector.setValue(m_vectorFields);

    std::vector<std::string>::iterator it = std::find(array.begin(), array.end(), val);
    if(!val.empty() && it != array.end())
        Vector.setValue(val.c_str());

    //recalculate the filter
    return Fem::FemPostFilter::execute();
}


void FemPostWarpVectorFilter::onChanged(const Property* prop) {

    if(prop == &Factor) {
        m_warp->SetScaleFactor(Factor.getValue());
    }
    else if(prop == &Vector && (Vector.getValue() >= 0)) {
        m_warp->SetInputArrayToProcess(0, 0, 0,
                                          vtkDataObject::FIELD_ASSOCIATION_POINTS, Vector.getValueAsString() );
    }

    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostWarpVectorFilter::mustExecute(void) const {

    if(Factor.isTouched() ||
       Vector.isTouched()) {

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}


PROPERTY_SOURCE(Fem::FemPostCutFilter, Fem::FemPostFilter)

FemPostCutFilter::FemPostCutFilter(void) : FemPostFilter() {

    ADD_PROPERTY_TYPE(Function, (0), "Cut", App::Prop_None, "The function object which defines the clip cut function");

    FilterPipeline clip;
    m_cutter            = vtkSmartPointer<vtkCutter>::New();
    clip.source         = m_cutter;
    clip.target         = m_cutter;
    addFilterPipeline(clip, "cut");
    setActiveFilterPipeline("cut");
}

FemPostCutFilter::~FemPostCutFilter() {

}

void FemPostCutFilter::onChanged(const Property* prop) {

    if(prop == &Function) {

        if(Function.getValue() && Function.getValue()->isDerivedFrom(FemPostFunction::getClassTypeId())) {
            m_cutter->SetCutFunction(static_cast<FemPostFunction*>(Function.getValue())->getImplicitFunction());
         }
    }

    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostCutFilter::mustExecute(void) const {

    if(Function.isTouched()) {

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

DocumentObjectExecReturn* FemPostCutFilter::execute(void) {

    if(!m_cutter->GetCutFunction())
        return StdReturn;

    return Fem::FemPostFilter::execute();
}

PROPERTY_SOURCE(Fem::FemPostGlyphFilter, Fem::FemPostFilter)

FemPostGlyphFilter::FemPostGlyphFilter(void): FemPostFilter() {

    ADD_PROPERTY_TYPE(Factor, (0), "Glyph", App::Prop_None, "The factor by which the Glyph is scaled and colored");
    ADD_PROPERTY_TYPE(Vector, (long(0)), "Glyph", App::Prop_None, "The field of vectors");
    ADD_PROPERTY_TYPE(GlyphType, (long(0)), "Glyph", App::Prop_None, "The selected glyph");

    arrowSource = vtkSmartPointer<vtkArrowSource>::New();
    glyphMethod = calcGlyphArrow;

    programmableGlyph = vtkSmartPointer<vtkProgrammableGlyphFilter>::New();
    programmableGlyph->SetSourceConnection(arrowSource->GetOutputPort());
    programmableGlyph->SetGlyphMethod(glyphMethod, this);

    namesGlyphTypes.push_back("Arrow (single-headed)");
    namesGlyphTypes.push_back("Arrow (double-headed)");

    m_glyphTypes.setEnums(namesGlyphTypes);
    GlyphType.setValue(m_glyphTypes);


    FilterPipeline glyph;

    glyph.source         = programmableGlyph;
    glyph.target         = programmableGlyph;
    addFilterPipeline(glyph, "glyph");
    setActiveFilterPipeline("glyph");
}

FemPostGlyphFilter::~FemPostGlyphFilter() {

}


DocumentObjectExecReturn* FemPostGlyphFilter::execute(void) {

    std::string val;
    if(m_vectorFields.getEnums() && Vector.getValue() >= 0)
        val = Vector.getValueAsString();

    std::vector<std::string> array;

    vtkSmartPointer<vtkDataObject> data = getInputData();
    if(!data || !data->IsA("vtkDataSet"))
        return StdReturn;

    vtkDataSet* dset = vtkDataSet::SafeDownCast(data);
    vtkPointData* pd = dset->GetPointData();

    for(int i=0; i<pd->GetNumberOfArrays(); ++i) {
        if(pd->GetArray(i)->GetNumberOfComponents()==3)
            array.push_back(pd->GetArrayName(i));
    }

    App::Enumeration empty;
    Vector.setValue(empty);
    m_vectorFields.setEnums(array);
    Vector.setValue(m_vectorFields);

    std::vector<std::string>::iterator it = std::find(array.begin(), array.end(), val);
    if(!val.empty() && it != array.end())
        Vector.setValue(val.c_str());

    //do the same with the glyphs
    std::string glyphVal;
    if(m_glyphTypes.getEnums() && GlyphType.getValue() >= 0)
        glyphVal = GlyphType.getValueAsString();

    std::vector<std::string>::iterator it2 = std::find(namesGlyphTypes.begin(), namesGlyphTypes.end(), glyphVal);
    if(!glyphVal.empty() && it2 != namesGlyphTypes.end())
       GlyphType.setValue(glyphVal.c_str());

    //recalculate the filter
    return Fem::FemPostFilter::execute();
}

void FemPostGlyphFilter::onChanged(const Property* prop)
{
    if (prop == &Factor) {
        scale = Factor.getValue();
    }
    else if (prop == &Vector && (Vector.getValue() >= 0)) {
        m_vectorFields.setValue(Vector.getValueAsString());
    }
    else if (prop == &GlyphType && (GlyphType.getValue() >= 0)) {
        std::string glyph = GlyphType.getValueAsString();
        if (m_glyphTypes.isValid()){
            m_glyphTypes.setValue(glyph);
            if (m_glyphTypes.isValue("Arrow (double-headed)")){
                doubleheaded= true;
                glyphMethod = calcGlyphArrow;
            }
            else if (m_glyphTypes.isValue("Arrow (single-headed)")){
                doubleheaded = false;
                glyphMethod = calcGlyphArrow;
            }
        }
    }

    //we need to modify the filter a bit, so that it knows something changed
    programmableGlyph->SetGlyphMethod(NULL, NULL);
    programmableGlyph->SetGlyphMethod(glyphMethod, this);

    Fem::FemPostFilter::onChanged(prop);
}

short int FemPostGlyphFilter::mustExecute(void) const {

    if(Factor.isTouched() ||
       Vector.isTouched() ||
       GlyphType.isTouched()) {

        return 1;
    }
    else return App::DocumentObject::mustExecute();
}

void FemPostGlyphFilter::calcGlyphArrow(void *arg){
    FemPostGlyphFilter *parent = (FemPostGlyphFilter*) arg;

    vtkProgrammableGlyphFilter *programmableGlyphFilter = (vtkProgrammableGlyphFilter*) parent->programmableGlyph;

    if (!programmableGlyphFilter)
    {
        return;
    }

    //aquire Data
    vtkPointData* pd = programmableGlyphFilter->GetPointData();
    const int pid = programmableGlyphFilter->GetPointId();

    //translation
    double position[3];
    programmableGlyphFilter->GetPoint(position);

    //scale
    const double scale = parent->scale;

    // if (pid == 0)
    //     std::cerr << "Vector: " << parent->m_vectorFields.getInt() << ", doubleheaded: " << parent->doubleheaded << ", Factor: " << scale << "\n";

    //orientation
    double orientvector[3];
    if (parent->m_vectorFields.isValid())
    {
        pd->GetArray(parent->m_vectorFields.getInt())->GetTuple(pid, orientvector);
    }
    else
    {
        return;
    }

    //magnitude
    const double magnitude = vtkMath::Norm(orientvector);
    //std::cerr << magnitude << std::endl;


    //global arrow with the parameters
    const vtkSmartPointer<vtkArrowSource> arrowSource = parent->arrowSource;

    //setup transformation
    vtkSmartPointer<vtkTransform> transform = vtkSmartPointer<vtkTransform>::New();
    transform->Identity();
    transform->Translate(position[0], position[1], position[2]);
    double vNew[3];

    // if statement from paraviews vtkArrowGlyphFilter.cxx
    if (magnitude > 0.0)
    {
        // if there is no y or z component
        if (orientvector[1] == 0.0 && orientvector[2] == 0.0)
        {
            if (orientvector[0] < 0)
            { // just flip x if we need to
                transform->RotateWXYZ(180.0,0,1,0);
            }
        }
        else
        {
            vNew[0] = (orientvector[0] + magnitude ) / 2.0 ;
            vNew[1] = orientvector[1] / 2.0;
            vNew[2] = orientvector[2] / 2.0;
            transform->RotateWXYZ(180.0, vNew[0], vNew[1], vNew[2]);
        }
    }
    //end -- thanks paraview
    transform->Update();

    vtkSmartPointer<vtkArrowSource> localArrow = vtkSmartPointer<vtkArrowSource>::New();
    vtkSmartPointer<vtkAlgorithm> glyph;
    if (parent->doubleheaded) {
        //take settings from arrowSource and scale them, so that the length is 1 again
        localArrow->SetTipLength(arrowSource->GetTipLength()*2.0);
        localArrow->SetTipRadius(arrowSource->GetTipRadius()*2.0);
        localArrow->SetTipResolution(arrowSource->GetTipResolution());
        localArrow->SetShaftRadius(arrowSource->GetShaftRadius()*2.0);
        localArrow->SetShaftResolution(arrowSource->GetShaftResolution());

        //inversion is only necessary if we're using double-headed arrows, since otherwise the orientation will do the inversion for us
        if (magnitude < 0)
            localArrow->InvertOn();

        localArrow->Update();

        //make the double-headed arrow
        vtkSmartPointer<vtkPolyData> arrow1 = vtkSmartPointer<vtkPolyData>::New();
        arrow1->ShallowCopy(localArrow->GetOutput());
        vtkSmartPointer<vtkTransform> transformArrow = vtkSmartPointer<vtkTransform>::New();
        transformArrow->Identity();
        transformArrow->RotateZ(180);
        transformArrow->Update();
        vtkSmartPointer<vtkTransformPolyDataFilter> transformArrowFilter = vtkSmartPointer<vtkTransformPolyDataFilter>::New();
        transformArrowFilter->SetTransform(transformArrow);
        transformArrowFilter->SetInputConnection(localArrow->GetOutputPort());
        transformArrowFilter->Update();
        vtkSmartPointer<vtkPolyData> arrow2 = vtkSmartPointer<vtkPolyData>::New();
        arrow2->ShallowCopy(transformArrowFilter->GetOutput());
        vtkSmartPointer<vtkAppendPolyData> doubleHeadedArrow = vtkSmartPointer<vtkAppendPolyData>::New();
        doubleHeadedArrow->AddInputData(arrow1);
        doubleHeadedArrow->AddInputData(arrow2);
        doubleHeadedArrow->Update();
        glyph = doubleHeadedArrow;

        transform->Scale(.5 * scale,.5 * scale,.5 * scale);
        transform->Update();
    }
    else {
        //just one arrow --> don't mess with scaling
        localArrow->SetTipLength(arrowSource->GetTipLength());
        localArrow->SetTipRadius(arrowSource->GetTipRadius());
        localArrow->SetTipResolution(arrowSource->GetTipResolution());
        localArrow->SetShaftRadius(arrowSource->GetShaftRadius());
        localArrow->SetShaftResolution(arrowSource->GetShaftResolution());
        localArrow->Update();
        glyph = localArrow;

        transform->Scale(scale,scale,scale);
        transform->Update();
    }

    //apply the transformation to the glyph
    vtkSmartPointer<vtkTransformFilter> transformFilter = vtkSmartPointer<vtkTransformFilter>::New();
    transformFilter->SetTransform(transform);
    transformFilter->SetInputConnection(glyph->GetOutputPort());
    transformFilter->Update();

    programmableGlyphFilter->SetSourceConnection(transformFilter->GetOutputPort());
}
