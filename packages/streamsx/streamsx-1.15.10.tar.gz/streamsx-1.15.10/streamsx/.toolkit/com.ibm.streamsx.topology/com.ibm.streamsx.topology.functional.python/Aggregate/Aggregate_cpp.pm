# SPL_CGT_INCLUDE: ../pyspltuple2tuple.cgt
# SPL_CGT_INCLUDE: ../pyspltuple2value.cgt
# SPL_CGT_INCLUDE: ../../opt/python/codegen/py_pyTupleTosplTuple.cgt
# SPL_CGT_INCLUDE: ../pyspltuple_constructor.cgt
# SPL_CGT_INCLUDE: ../pyspltuple.cgt
# SPL_CGT_INCLUDE: ../../opt/python/codegen/py_splTupleCheckForBlobs.cgt
# SPL_CGT_INCLUDE: ../pyspltuple2dict.cgt

package Aggregate_cpp;
use strict; use Cwd 'realpath';  use File::Basename;  use lib dirname(__FILE__);  use SPL::Operator::Instance::OperatorInstance; use SPL::Operator::Instance::Annotation; use SPL::Operator::Instance::Context; use SPL::Operator::Instance::Expression; use SPL::Operator::Instance::ExpressionTree; use SPL::Operator::Instance::ExpressionTreeEvaluator; use SPL::Operator::Instance::ExpressionTreeVisitor; use SPL::Operator::Instance::ExpressionTreeCppGenVisitor; use SPL::Operator::Instance::InputAttribute; use SPL::Operator::Instance::InputPort; use SPL::Operator::Instance::OutputAttribute; use SPL::Operator::Instance::OutputPort; use SPL::Operator::Instance::Parameter; use SPL::Operator::Instance::StateVariable; use SPL::Operator::Instance::TupleValue; use SPL::Operator::Instance::Window; 
sub main::generate($$) {
   my ($xml, $signature) = @_;  
   print "// $$signature\n";
   my $model = SPL::Operator::Instance::OperatorInstance->new($$xml);
   unshift @INC, dirname ($model->getContext()->getOperatorDirectory()) . "/../impl/nl/include";
   $SPL::CodeGenHelper::verboseMode = $model->getContext()->isVerboseModeOn();
   SPL::CodeGen::implementationPrologue($model);
   print "\n";
   print "\n";
    # Generic setup of a variety of variables to
    # handle conversion of spl tuples to/from Python
   
    my $tkdir = $model->getContext()->getToolkitDirectory();
    my $pydir = $tkdir."/opt/python";
   
    require $pydir."/codegen/splpy.pm";
   
    # Initialize splpy.pm
    splpyInit($model);
   
    # Currently function operators only have a single input port
    # and take all the input attributes
    my $iport = $model->getInputPortAt(0);
    my $inputAttrs2Py = $iport->getNumberOfAttributes();
   
    # determine which input tuple style is being used
    my $pystyle = $model->getParameterByName("pyStyle");
    if ($pystyle) {
        $pystyle = substr($pystyle->getValueAt(0)->getSPLExpression(), 1, -1);
    } else {
        $pystyle = splpy_tuplestyle($model->getInputPortAt(0));
    }
    # $pystyle is the raw value from the operator parameter
    # $pystyle_nt is the value that defines how the function is called
    # (for style namedtuple:xxxx it is tuple)
    # $pystyle_nt is non-zero if style is namedtuple
    my $pystyle_fn = $pystyle;
    my $pystyle_nt = substr($pystyle, 0, 11) eq 'namedtuple:';
    if ($pystyle_nt) {
       $pystyle_fn = 'tuple';
    }
   print "\n";
   print "\n";
   
   #
   # Locking
   #
   # If a window has real-time based policies then window acquire
   # data is used as locking. In this case the window object itself
   # gets all the locking.
   #
   # Otherwise if the window has a state handler then an AutoMutex
   # is used to provide locking between tuple/punct processing and
   # state handler methods.
   #
   # Otherwise tuple/punct processing is protected by an AutoPortMutex.
   
   # Configure Windowing
    my $inputPort = $model->getInputPortAt(0); 
    my $window = $inputPort->getWindow();
    my $windowCppInitializer = SPL::CodeGen::getWindowCppInitializer($window,"PyObject *");
   
    # Select the Python wrapper function
    my $pyoutstyle = splpy_tuplestyle($model->getOutputPortAt(0));
   
    my $out_pywrapfunc=  'object_in__' . $pyoutstyle . '_out';
   print "\n";
   print "\n";
   print '#define SPLPY_AGGREGATE(f, v, r, occ) \\', "\n";
   print '    streamsx::topology::Splpy::pyTupleMap(f, v, r)', "\n";
   print "\n";
   print 'MY_OPERATOR_SCOPE::MY_OPERATOR::MY_OPERATOR() :', "\n";
   print '   funcop_(NULL),', "\n";
   print '   pyInStyleObj_(NULL),', "\n";
   if ($pyoutstyle eq 'dict') {
   print '    ', "\n";
   print '   pyOutNames_0(NULL),', "\n";
   }
   print '    ', "\n";
   print '   loads(NULL),', "\n";
   print '   occ_(-1),', "\n";
   print '   window_(';
   print $windowCppInitializer;
   print '),', "\n";
   print '   _partitionCount(getContext().getMetrics().getCustomMetricByName("nCurrentPartitions"))', "\n";
   print '   ', "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '   , partitionStateHandler_(NULL)', "\n";
   print '#endif', "\n";
   print '{', "\n";
    if ($window->isSliding()) {
   print "\n";
   print '    window_.registerOnWindowTriggerHandler(this);', "\n";
   print '    window_.registerAfterTupleEvictionHandler(this);', "\n";
   }
   print "\n";
    if ($window->isTumbling()) {
   print "\n";
   print '    window_.registerBeforeWindowFlushHandler(this);', "\n";
   }
   print "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print '    window_.registerOnWindowPartitionEviction(this);', "\n";
   print '#endif', "\n";
   print "\n";
   print '#if SPLPY_OP_STATE_HANDLER == 1', "\n";
   print '    window_.registerSerializationHandler(this);', "\n";
   print '#endif', "\n";
   print "\n";
   print '    const char * out_wrapfn = "';
   print $out_pywrapfunc;
   print '";', "\n";
   # If occ parameter is positive then pass-by-ref is possible
   # Generate code to allow pass by ref but only use when
   # not connected to a PE output port.
   
    my $oc = $model->getParameterByName("outputConnections");
   
    if ($oc) {
       my $occ = $oc->getValueAt(0)->getSPLExpression();
       if ($occ > 0) {
           my $pybyrefwrapfunc = 'object_in__object_out';
   print "\n";
   print "\n";
   print '#undef SPLPY_AGGREGATE', "\n";
   print '#define SPLPY_AGGREGATE(f, v, r, occ) \\', "\n";
   print '    streamsx::topology::Splpy::pyTupleMapByRef(f, v, r, occ)', "\n";
   print "\n";
   print '    if (!this->getOutputPortAt(0).isConnectedToAPEOutputPort()) {', "\n";
   print '       // pass by reference', "\n";
   print '       out_wrapfn = "';
   print $pybyrefwrapfunc;
   print '";', "\n";
   print '       occ_ = ';
   print $occ;
   print ';', "\n";
   print '    }', "\n";
       } 
   
       
    }
   print "\n";
   print '    _partitionCount.setValueNoLock(0);', "\n";
   print "\n";
   print '    funcop_ = new SplpyFuncOp(this, SPLPY_CALLABLE_STATE_HANDLER, out_wrapfn);', "\n";
   print "\n";
    if ($pystyle_fn eq 'dict') { 
   print "\n";
   print '#define pyInNames_ pyInStyleObj_', "\n";
   print '{', "\n";
   print '     SplpyGIL lock;', "\n";
   print '     pyInNames_ = streamsx::topology::Splpy::pyAttributeNames(', "\n";
   print '               getInputPortAt(0));', "\n";
   print '}', "\n";
    } 
   print "\n";
   print "\n";
    if ($pystyle_nt) { 
   print "\n";
   print '#define pyNamedtupleCls_ pyInStyleObj_', "\n";
   print '{', "\n";
   print '     SplpyGIL lock;', "\n";
   print '     pyNamedtupleCls_ = streamsx::topology::SplpyGeneral::callFunction(', "\n";
   print '        "streamsx.topology.runtime", "_get_namedtuple_cls",', "\n";
   print '       streamsx::topology::pyUnicode_FromUTF8("';
   print $iport->getSPLTupleType();
   print '"),', "\n";
   print '       streamsx::topology::pyUnicode_FromUTF8("';
   print substr($pystyle, 11);
   print '"));', "\n";
   print '}', "\n";
    } 
   print "\n";
   print '    ', "\n";
   print '    // Obtain the function that loads the tuple\'s value in process()', "\n";
   print '    {', "\n";
   print '    SplpyGIL lock;', "\n";
   print '    ';
   if ($pyoutstyle eq 'dict') {
   print "\n";
   print '    pyOutNames_0 = Splpy::pyAttributeNames(getOutputPortAt(0));', "\n";
   print '    ';
   }
   print '    ', "\n";
   print '    ';
   if ($pystyle eq 'pickle'){
   print "\n";
   print '    loads = SplpyGeneral::loadFunction("pickle", "loads");', "\n";
   print '    ';
    } elsif ($pystyle eq 'json'){ 
   print "\n";
   print '    loads = SplpyGeneral::loadFunction("json", "loads");', "\n";
   print '    ';
    } 
   print "\n";
   print '    }', "\n";
   print '#if SPLPY_OP_STATE_HANDLER == 1', "\n";
   print '   this->getContext().registerStateHandler(*this);', "\n";
   print '#endif', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print '    // This is based on SplpyFuncOp::loadAndWrapCallable', "\n";
   print '    SplpyGIL lock;', "\n";
   print '    setOp(this);', "\n";
   print "\n";
   print '    // The object to be called is either partitionCallable for', "\n";
   print '    // a function passed into the operator', "\n";
   print '    // or a pickled encoded class instance', "\n";
   print '    // represented as a string in parameter pyPartitionByCallable', "\n";
   print '    ', "\n";
   print '#if SPLPY_PARTITION_BY_CALLABLE == 1', "\n";
   print "\n";
   print '    // argument is the serialized callable instance', "\n";
   print '    PyObject * partitionCallable = pyUnicode_FromUTF8(param("pyPartitionByCallable").c_str());', "\n";
   print "\n";
   print '    // base64.decode', "\n";
   print '    PyObject * decoded = SplpyGeneral::callFunction("base64","b64decode", partitionCallable, NULL);', "\n";
   print "\n";
   print '    // dill.loads', "\n";
   print '    PyObject * loaded = SplpyGeneral::callFunction("dill", "loads", decoded, NULL);', "\n";
   print '       ', "\n";
   print '    setCallable(loaded);', "\n";
   print "\n";
   print '#else', "\n";
   print '    ', "\n";
   print '    setCallable( ', "\n";
   print '        SplpyGeneral::loadFunction(param("pyPartitionByModule"), param("pyPartitionByName")));', "\n";
   print "\n";
   print '#endif // SPLPY_PARTITION_BY_CALLABLE', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '    partitionStateHandler_ = new SplpyOpStateHandlerImpl(this);', "\n";
   print '#endif', "\n";
   print "\n";
   print '#endif // SPLPY_PARTITION_BY_PYTHON', "\n";
   print '}', "\n";
   print "\n";
   print 'MY_OPERATOR_SCOPE::MY_OPERATOR::~MY_OPERATOR() ', "\n";
   print '{', "\n";
   print '  ';
   if ($pyoutstyle eq 'dict') {
   print ' ', "\n";
   print '  {', "\n";
   print '    SplpyGIL lock;', "\n";
   print '    Py_CLEAR(pyOutNames_0);', "\n";
   print '  }', "\n";
   print '  ';
   }
   print '  	', "\n";
   print '  delete funcop_;', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '    delete partitionStateHandler_;', "\n";
   print '#endif', "\n";
   print "\n";
   print '  ';
    if (($pystyle eq 'json') || ($pystyle eq 'pickle')) {
   print "\n";
   print '  {', "\n";
   print '      SplpyGIL lock;', "\n";
   print '      Py_CLEAR(loads);', "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1 ', "\n";
   print '      clearOp();', "\n";
   print '      clearCallable();', "\n";
   print '#endif', "\n";
   print '  }', "\n";
   print '  ';
    } 
   print "\n";
   print '  ', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::prepareToShutdown() ', "\n";
   print '{', "\n";
   print '    funcop_->prepareToShutdown();', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::process(Tuple const & tuple, uint32_t port)', "\n";
   print '{', "\n";
   # Takes the input SPL tuple and converts it to
   # the arguments needed to be passed to a Python
   # functional operator
   
   # Variables that need to be set:
   
   # $pyStyle - tuple or dictionary
   # $iport - input port 
   # $inputAttrs2Py - number of attributes to pass as tuple style
   print "\n";
   print "\n";
   print '    ';
   print $iport->getCppTupleType();
   print ' const & ';
   print $iport->getCppTupleName();
   print ' = static_cast< ';
   print $iport->getCppTupleType();
   print ' const &>(tuple);', "\n";
   print "\n";
   print splpy_inputtuple2value($pystyle, $iport);
   
   if ($pystyle eq 'dict' || $pystyle eq 'tuple' || $pystyle_nt) {
   print "\n";
   # Perl Variables that need to be set:
   #
   # $iport - input port 
   #
   # $inputAttrs2Py - number of attributes to pass as tuple style
   #
   
      #Check if a blob exists in the input schema
      for (my $i = 0; $i < $inputAttrs2Py; ++$i) {
         if (typeHasBlobs($iport->getAttributeAt($i)->getSPLType())) {
   print "\n";
   print '   PYSPL_MEMORY_VIEW_CLEANUP();', "\n";
            last;
         }
      }
   print "\n";
   }
   
   if ($pystyle eq 'dict') {
   print "\n";
   # Takes the input SPL tuple and converts it to
   # as a dict to be passed to a Python functional operator
   #
   # Leaves the C++ variable value set to a PyObject * dict.
   
   # Variables that need to be set:
   # $iport - input port 
   print "\n";
   print "\n";
   print '  PyObject *value = 0;', "\n";
   print '  {', "\n";
   print '  SplpyGIL lockdict;', "\n";
   print '  PyObject * pyDict = PyDict_New();', "\n";
        for (my $i = 0; $i < $inputAttrs2Py; ++$i) {
            my $la = $iport->getAttributeAt($i);
            print convertAndAddToPythonDictionaryObject($iport->getCppTupleName(), $i, $la->getSPLType(), $la->getName(), 'pyInNames_');
        }
   print "\n";
   print '  value = pyDict;', "\n";
   print '  }', "\n";
    } elsif ($pystyle eq 'tuple' || $pystyle_nt) { 
   print "\n";
   # Takes the input SPL tuple and converts it to
   # as a tuple to be passed to a Python functional operator
   #
   # Leaves the C++ variable value set to a PyObject * tuple.
   
   # Variables that need to be set:
   # $iport - input port 
   print "\n";
   print "\n";
   print '  PyObject *value = 0;', "\n";
   print '  {', "\n";
   print '  SplpyGIL locktuple;', "\n";
   print '  PyObject * pyTuple = PyTuple_New(';
   print $inputAttrs2Py;
   print ');', "\n";
        for (my $i = 0; $i < $inputAttrs2Py; ++$i) {
            my $la = $iport->getAttributeAt($i);
            print convertAndAddToPythonTupleObject($iport->getCppTupleName(), $i, $la->getSPLType(), $la->getName());
        }
   print "\n";
    if ($pystyle_nt) { 
   print "\n";
   print '    pyTuple = streamsx::topology::SplpyGeneral::pyCallObject(pyNamedtupleCls_, pyTuple);', "\n";
   print "\n";
    } 
   print "\n";
   print "\n";
   print '  value = pyTuple;', "\n";
   print '  }', "\n";
    } 
   print "\n";
   print "\n";
   print '  PyObject *python_value;', "\n";
   print "\n";
   print '  // If the input style is pickle,', "\n";
   print "\n";
   print '  // None of the streamsx::topology methods in this scope grab the lock', "\n";
   print '  // so we need to do it here.', "\n";
   print '  ', "\n";
   print '  ';
   if ($pystyle eq 'pickle'){
   print "\n";
   print '      unsigned char const *data = value.getData();', "\n";
   print '      unsigned char fmt = *data;', "\n";
   print '      if (fmt == STREAMSX_TPP_PTR) {', "\n";
   print '          __SPLTuplePyPtr *stp = (__SPLTuplePyPtr *)(data);', "\n";
   print '          python_value = stp->pyptr;', "\n";
   print '      }', "\n";
   print '      // Anything ASCII is also Pickle (Python 2 default format)', "\n";
   print '      else if (fmt <= STREAMSX_TPP_PICKLE) {', "\n";
   print '      	  // This is a pickled value. Need to depickle it.', "\n";
   print '	  {', "\n";
   print '	      SplpyGIL lock; ', "\n";
   print '              python_value = pySplValueToPyObject(value);', "\n";
   print "\n";
   print '	      // Depickle the tuple.', "\n";
   print '	      PyObject *tup = PyTuple_New(1);', "\n";
   print '	      PyTuple_SET_ITEM(tup, 0, python_value);', "\n";
   print '   	      python_value = SplpyGeneral::pyCallObject(loads, tup);', "\n";
   print "\n";
   print '	  } // End SplpyGIL lock', "\n";
   print '      }', "\n";
   print '  ';
    } elsif ($pystyle eq 'string'){
   print "\n";
   print '      {', "\n";
   print '	  SplpyGIL lock;', "\n";
   print '          python_value = pySplValueToPyObject(value);', "\n";
   print '      }', "\n";
   print '  ';
    } elsif ($pystyle eq 'json'){
   print "\n";
   print '      {', "\n";
   print '      	  SplpyGIL lock;', "\n";
   print '          python_value = pySplValueToPyObject(value);', "\n";
   print '	  PyObject *tup = PyTuple_New(1);', "\n";
   print '	  PyTuple_SET_ITEM(tup, 0, python_value);', "\n";
   print '	  python_value = SplpyGeneral::pyCallObject(loads, tup);', "\n";
   print '      }', "\n";
   print '  ';
    } elsif ($pystyle eq 'dict' || $pystyle eq 'tuple' || $pystyle_nt) {
   print "\n";
   print '      python_value = value;', "\n";
   print ' ';
    } else{
   	  SPL::CodeGen::exitln($pystyle . " is an unsupported input type.");      
       }
    
   print "\n";
   print "\n";
   print "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 1', "\n";
   print '   // window_.insert() obtains the mutex.', "\n";
   print '#elif SPLPY_OP_STATE_HANDLER == 1', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#else', "\n";
   print '    SPL::AutoPortMutex am(mutex_, *this);', "\n";
   print '#endif', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_BY_ATTRIBUTE == 1', "\n";
   print '  PartitionType const & partition = getPartitionValue(static_cast<TupleType const &>(tuple));', "\n";
   print '  window_.insert(python_value, partition);', "\n";
   print '#elif SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print '  PartitionType const & partition = getPartitionValue(python_value);', "\n";
   print '  window_.insert(python_value, partition);', "\n";
   print '#else', "\n";
   print '  window_.insert(python_value);', "\n";
   print '#endif', "\n";
   print "\n";
   print '  _partitionCount.setValueNoLock(window_.getWindowStorage().size());', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::process(Punctuation const & punct, uint32_t port)', "\n";
   print '{', "\n";
    if ($window->isTumbling()) {
   print "\n";
   print '   // Aggregate the remaining contents if there are some.', "\n";
   print '   if (punct == Punctuation::FinalMarker)', "\n";
   print '       aggregateRemaining();', "\n";
   }
   print "\n";
   print '}', "\n";
   print "\n";
    if ($window->isTumbling()) {
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::aggregateRemaining() {', "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 1', "\n";
   print '    SPL::AutoWindowDataAcquirer<WindowType::TupleType, WindowType::PartitionType, WindowType::DataType, WindowType::StorageType> awd(window_);', "\n";
   print '#elif SPLPY_OP_STATE_HANDLER == 1', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#else', "\n";
   print '    SPL::AutoPortMutex am(mutex_, *this);', "\n";
   print '#endif', "\n";
   print '    WindowType::StorageType & storage = window_.getWindowStorage();', "\n";
   print '    // Iterate through the partitions.', "\n";
   print '    for (WindowType::StorageType::iterator partition = storage.begin(); partition != storage.end(); ++partition) {', "\n";
   print '        WindowType::DataType & content = partition->second;', "\n";
   print '	if (!content.empty()) {', "\n";
   print '            beforeWindowFlushEvent(window_, partition->first);', "\n";
   print "\n";
   print '           // Since we have processed these tuples in batch', "\n";
   print '           // don\'t process them again. ', "\n";
   print '           content.clear();', "\n";
   print '        }', "\n";
   print '    }', "\n";
   print '}', "\n";
   }
   print "\n";
   print "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print 'PyObject * MY_OPERATOR_SCOPE::MY_OPERATOR::getPartitionValue(PyObject * tuple) const {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "getPartitionValue: enter", SPLPY_SH_ASPECT);', "\n";
   print '    SplpyGIL lock; ', "\n";
   print '    PyObject * arg = PyTuple_New(1);', "\n";
   print '    Py_INCREF(tuple);', "\n";
   print '    PyTuple_SET_ITEM(arg, 0, tuple);', "\n";
   print '    SPLAPPTRC(L_DEBUG, "getPartitionValue: pyCallObject", SPLPY_SH_ASPECT);', "\n";
   print '    PyObject *ret = SplpyGeneral::pyCallObject(callable(), arg);', "\n";
   print "\n";
   print '    if (!ret) {', "\n";
   print '        SplpyGeneral::tracePythonError();        ', "\n";
   print '        throw SplpyExceptionInfo::pythonError("partition").exception();', "\n";
   print '    }', "\n";
   print "\n";
   print '    SPLAPPTRC(L_DEBUG, "getPartitionValue: exit", SPLPY_SH_ASPECT);', "\n";
   print '    return ret;', "\n";
   print '}', "\n";
   print '#endif // SPLPY_PARTITION_BY_PYTHON', "\n";
   print "\n";
   print '// ##############################', "\n";
   print '// Window Event Handler Overrides', "\n";
   print '// ##############################', "\n";
   print "\n";
    if ($window->isSliding()) {
   print "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::afterTupleEvictionEvent(', "\n";
   print '     WindowEventType::WindowType & window,  WindowEventType::TupleType & tuple,  WindowEventType::PartitionType const & partition) {', "\n";
   print '     // Drop reference to tuple after it is removed from the window.', "\n";
   print '     SplpyGIL lock;', "\n";
   print '     Py_DECREF(tuple);', "\n";
   print '}', "\n";
   print "\n";
   }
   print "\n";
   print "\n";
   print '// Perform the aggregation.', "\n";
    if ($window->isSliding()) {
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::onWindowTriggerEvent(', "\n";
   }
   print "\n";
    if ($window->isTumbling()) {
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::beforeWindowFlushEvent(', "\n";
   }
   print "\n";
   print '    WindowEventType::WindowType & window, WindowEventType::PartitionType const & key){    ', "\n";
   print '    SPLAPPTRC(L_DEBUG, "aggregation: enter", SPLPY_SH_ASPECT);', "\n";
   print '    WindowType::StorageType & storage = window.getWindowStorage();', "\n";
   print "\n";
   print '    WindowType::DataType & content = storage[key];', "\n";
   print '    PyObject *items;', "\n";
   print '    {', "\n";
   print '      SplpyGIL lock;', "\n";
   print '      items = PyList_New(content.size());', "\n";
   print '      unsigned int idx = 0;', "\n";
   print '      for(WindowType::DataType::iterator it=content.begin(); it!=content.end(); ++it) {', "\n";
   print '        PyObject *item = *it;', "\n";
    if ($window->isSliding()) {
   print "\n";
   print '	// The list steals a reference, increment such that the window can maintain a copy', "\n";
   print '	// once the tuple is deleted. Woith tumbling the window does', "\n";
   print '        // retain the contents.', "\n";
   print '	Py_INCREF(item);', "\n";
   }
   print "\n";
   print '	PyList_SET_ITEM(items, idx, item);', "\n";
   print '	++idx;', "\n";
   print '      }', "\n";
   print '    }', "\n";
   print '  OPort0Type otuple;', "\n";
   print "\n";
   print '  {', "\n";
   print '    try {', "\n";
   print '      SplpyGIL lock;', "\n";
   print '      SPLAPPTRC(L_DEBUG, "aggregation: call", SPLPY_SH_ASPECT);', "\n";
   print '      ';
   if ($pyoutstyle eq 'dict') {
   print "\n";
   print '	    PyObject * ret = streamsx::topology::Splpy::pyTupleMap(funcop_->callable(), items);', "\n";
   print '	    if (ret == NULL)', "\n";
   print '		  return;', "\n";
   print '	    if (PyTuple_Check(ret)) {', "\n";
   print '		  fromPyTupleToSPLTuple(ret, otuple);', "\n";
   print '		  Py_DECREF(ret);', "\n";
   print '	    } else if (PyDict_Check(ret)) {', "\n";
   print '		  fromPyDictToSPLTuple(ret, otuple);', "\n";
   print '		  Py_DECREF(ret);', "\n";
   print '	    } else {', "\n";
   print '		  throw SplpyGeneral::generalException("submit",', "\n";
   print '		   "Fatal error: Value submitted must be a Python tuple or dict.");', "\n";
   print '	    }', "\n";
   print '	  SPLAPPTRC(L_DEBUG, "aggregation: submit", SPLPY_SH_ASPECT);', "\n";
   print '      submit(otuple, 0);', "\n";
   print '      ';
    } else { 
   print "\n";
   print '      if (SPLPY_AGGREGATE(funcop_->callable(), items,', "\n";
   print '        otuple.get_';
   print $model->getOutputPortAt(0)->getAttributeAt(0)->getName();
   print '(), occ_)){', "\n";
   print '        SPLAPPTRC(L_DEBUG, "aggregation: submit", SPLPY_SH_ASPECT);', "\n";
   print '        submit(otuple, 0);', "\n";
   print '      } ', "\n";
   print '      else {', "\n";
   print '        SPLAPPTRC(L_DEBUG, "aggregation: fail", SPLPY_SH_ASPECT);', "\n";
   print '      }	   ', "\n";
   print '      ';
   }
   print "\n";
   print '    } catch (const streamsx::topology::SplpyExceptionInfo& excInfo) {', "\n";
   print '      SPLAPPTRC(L_DEBUG, "aggregation: caught", SPLPY_SH_ASPECT);', "\n";
   print '      SPLPY_OP_HANDLE_EXCEPTION_INFO_GIL(excInfo);', "\n";
   print '      return;', "\n";
   print '    }', "\n";
   print '    submit(Punctuation::WindowMarker, 0);', "\n";
   print '  }', "\n";
   print '  SPLAPPTRC(L_DEBUG, "aggregation: exit", SPLPY_SH_ASPECT);', "\n";
   print '}', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::onWindowPartitionEviction(WindowEventType::WindowType & window, WindowEventType::PartitionIterator begin, WindowEventType::PartitionIterator end) {', "\n";
   print '  SplpyGIL lock;', "\n";
   print '  ', "\n";
   print '  for (WindowEventType::PartitionIterator it = begin; it != end; ++it) {', "\n";
   print '    Py_XDECREF(it->first);', "\n";
   print '  }', "\n";
   print '}', "\n";
   print '#endif', "\n";
   print "\n";
   print '// ##################################', "\n";
   print '// End Window Event Handler Overrides', "\n";
   print '// ##################################', "\n";
   print "\n";
   print '#if SPLPY_OP_STATE_HANDLER == 1', "\n";
   print "\n";
   print '/* StateHandler methods */', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::drain() {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "drain-Aggregate: enter", SPLPY_SH_ASPECT);', "\n";
    if ($window->isTumbling()) {
   print "\n";
   print '   aggregateRemaining();', "\n";
   }
   print "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 0', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#endif', "\n";
   print '    window_.drain();', "\n";
   print '    SPLAPPTRC(L_DEBUG, "drain-Aggregate: exit", SPLPY_SH_ASPECT);', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::checkpoint(SPL::Checkpoint & ckpt) {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "checkpoint-Aggregate: enter", SPLPY_SH_ASPECT);', "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 0', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#endif', "\n";
   print '    window_.checkpoint(ckpt);', "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '    try {', "\n";
   print '        partitionStateHandler_->checkpoint(ckpt);', "\n";
   print '    }', "\n";
   print '    catch (SplpyExceptionInfo const & e) {', "\n";
   print '        throw e.exception();', "\n";
   print '    }', "\n";
   print '#endif	', "\n";
   print '    SPLAPPTRC(L_DEBUG, "checkpoint-Aggregate: exit", SPLPY_SH_ASPECT);', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::reset(SPL::Checkpoint & ckpt) {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "reset-Aggregate: enter", SPLPY_SH_ASPECT);', "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 0', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#endif', "\n";
   print '    window_.reset(ckpt);', "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '    try {', "\n";
   print '        partitionStateHandler_->reset(ckpt);', "\n";
   print '    }', "\n";
   print '    catch (SplpyExceptionInfo const & e) {', "\n";
   print '        throw e.exception();', "\n";
   print '    }', "\n";
   print '#endif', "\n";
   print '    SPLAPPTRC(L_DEBUG, "reset-Aggregate: exit", SPLPY_SH_ASPECT);', "\n";
   print '}', "\n";
   print "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::resetToInitialState() {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "resetToInitialState-Aggregate: enter", SPLPY_SH_ASPECT);', "\n";
   print '#if SPLPY_AGGREGATE_TIME_POLICIES == 0', "\n";
   print '    SPL::AutoMutex am(mutex_);', "\n";
   print '#endif', "\n";
   print '    window_.resetToInitialState();', "\n";
   print '#if SPLPY_PARTITION_IS_STATEFUL == 1', "\n";
   print '    try {', "\n";
   print '        partitionStateHandler_->resetToInitialState();', "\n";
   print '    }', "\n";
   print '    catch (SplpyExceptionInfo const & e) {', "\n";
   print '        throw e.exception();', "\n";
   print '    }', "\n";
   print '#endif', "\n";
   print '    SPLAPPTRC(L_DEBUG, "resetToInitialState-Aggregate: exit", SPLPY_SH_ASPECT);', "\n";
   print '}', "\n";
   print "\n";
   print '#endif', "\n";
   print "\n";
   print '#if SPLPY_PARTITION_BY_PYTHON == 1', "\n";
   print '  void MY_OPERATOR_SCOPE::MY_OPERATOR::setCallable(PyObject * callable) {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "setCallable: enter", SPLPY_SH_ASPECT);', "\n";
   print '    Py_CLEAR(callable_);', "\n";
   print '    callable_ = callable;', "\n";
   print '    Py_INCREF(callable);', "\n";
   print '    SPLAPPTRC(L_DEBUG, "setCallable: exit", SPLPY_SH_ASPECT);', "\n";
   print '  } ', "\n";
   print '  void MY_OPERATOR_SCOPE::MY_OPERATOR::clearCallable() {', "\n";
   print '    SPLAPPTRC(L_DEBUG, "clearCallable: enter", SPLPY_SH_ASPECT);', "\n";
   print '    Py_CLEAR(callable_);', "\n";
   print '    SPLAPPTRC(L_DEBUG, "clearCallable: exit", SPLPY_SH_ASPECT);', "\n";
   print '  }', "\n";
   print "\n";
   print '#endif', "\n";
   print "\n";
     if ($pyoutstyle eq 'dict') {
   	my %cpp_tuple_types;  
       # In this case we don't want the function that
       # converts the Python tuple to an SPL tuple to
       # copy attributes from the input port
       my $iport;
   
       my $oport = $model->getOutputPortAt(0);
       my $oport_submission = 0;
       my $otupleType = $oport->getSPLTupleType();
       my @onames = SPL::CodeGen::Type::getAttributeNames($otupleType);
       my @otypes = SPL::CodeGen::Type::getAttributeTypes($otupleType);
   
   print "\n";
   print '// Create member function that converts Python tuple to SPL tuple', "\n";
   # Generates functions in an operator that converts a Python
   # tuple to an SPL tuple for a given port and optional to
   # submit the tuple.
   #
   # $oport must be set on entry to required output port
   # $oport_submission must be set on entry to generate submission methods.
   # $iport can be set to automatically copy input attributes to
   # output attributes when the Python tuple does not supply a value.
   
     my $itypeparam = "";
     my $itypearg = "";
     if (defined $iport) {
        $itypeparam = ", " . $iport->getCppTupleType() . " const & ituple";
        $itypearg = ", ituple";
     }
   print "\n";
   print "\n";
    if ($oport_submission) { 
   print "\n";
   print ' ', "\n";
   print '// Python tuple to SPL tuple with submission to a port', "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::fromPythonToPort';
   print $oport->getIndex();
   print '(PyObject *pyTuple, ';
   print $oport->getCppTupleType();
   print ' & otuple ';
   print $itypeparam;
   print ') {', "\n";
   print "\n";
   print '  try {', "\n";
   print '    MY_OPERATOR_SCOPE::MY_OPERATOR::fromPyTupleToSPLTuple(pyTuple, otuple ';
   print $itypearg;
   print ');', "\n";
   print '  } catch (const streamsx::topology::SplpyExceptionInfo& excInfo) {', "\n";
   print '    SPLPY_OP_HANDLE_EXCEPTION_INFO(excInfo);', "\n";
   print '    return;', "\n";
   print '  }', "\n";
   print "\n";
   print '  STREAMSX_TUPLE_SUBMIT_ALLOW_THREADS(otuple, ';
   print $oport->getIndex();
   print ');', "\n";
   print '}', "\n";
   print "\n";
   print '// Python dict to SPL tuple with submission to a port.', "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::fromPythonDictToPort';
   print $oport->getIndex();
   print '(PyObject *pyDict, ';
   print $oport->getCppTupleType();
   print ' & otuple ';
   print $itypeparam;
   print ') {', "\n";
   print "\n";
   print '  try {', "\n";
   print '    MY_OPERATOR_SCOPE::MY_OPERATOR::fromPyDictToSPLTuple(pyDict, otuple ';
   print $itypearg;
   print ');', "\n";
   print '  } catch (const streamsx::topology::SplpyExceptionInfo& excInfo) {', "\n";
   print '    SPLPY_OP_HANDLE_EXCEPTION_INFO(excInfo);', "\n";
   print '    return;', "\n";
   print '  }', "\n";
   print "\n";
   print '  STREAMSX_TUPLE_SUBMIT_ALLOW_THREADS(otuple, ';
   print $oport->getIndex();
   print ');', "\n";
   print '}', "\n";
   print "\n";
   }
   print "\n";
   print "\n";
   # Ensure we generate function only once for each tuple type
   my $otype = $oport->getCppTupleType();
   if (! exists $cpp_tuple_types{$otype}) {
       $cpp_tuple_types{$otype} = 1;
   print "\n";
   print "\n";
   print '// Python tuple to SPL tuple , conversion only', "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::fromPyTupleToSPLTuple(PyObject *pyTuple, ';
   print $oport->getCppTupleType();
   print ' & otuple  ';
   print $itypeparam;
   print ') {', "\n";
   print "\n";
   print '  Py_ssize_t frs = PyTuple_GET_SIZE(pyTuple); ', "\n";
   print '    ', "\n";
     if (defined $iport) {
       print 'bool setAttr = false;';
     }
   
     for (my $ai = 0; $ai < $oport->getNumberOfAttributes(); ++$ai) {
       
       my $attribute = $oport->getAttributeAt($ai);
       my $name = $attribute->getName();
       my $atype = $attribute->getSPLType();
       splToPythonConversionCheck($atype);
       
       if (defined $iport) {
                print 'setAttr = false;';
       }
   print "\n";
   print '    if (';
   print $ai;
   print ' < frs) {', "\n";
   print '         // Value from the Python function', "\n";
   print '         PyObject *pyAttrValue = PyTuple_GET_ITEM(pyTuple, ';
   print $ai;
   print ');', "\n";
   print '         if (!SplpyGeneral::isNone(pyAttrValue)) {', "\n";
   print '                  streamsx::topology::pySplValueFromPyObject(', "\n";
   print '                               otuple.get_';
   print $name;
   print '(), pyAttrValue);', "\n";
       if (defined $iport) {
                print 'setAttr = true;';
       }
   print "\n";
   print '      }', "\n";
   print '   }', "\n";
       if (defined $iport) {
       
       # Only copy attributes across if they match on name and type,
       # or on name and input type T and output type optional<T>
       my $matchInputAttr = $iport->getAttributeByName($name);
       if (defined $matchInputAttr) {
           my $inputType = $matchInputAttr->getSPLType();
           if (($inputType eq $atype) ||
               (hasOptionalTypesSupport() &&
                SPL::CodeGen::Type::isOptional($atype) &&
                ($inputType eq
                 SPL::CodeGen::Type::getUnderlyingType($atype)))) {
   print "\n";
   print '    if (!setAttr) {', "\n";
   print '      // value from the input attribute', "\n";
   print '      otuple.set_';
   print $name;
   print '(ituple.get_';
   print $name;
   print '());', "\n";
   print '    }', "\n";
         }
       }
      }
   print "\n";
   print '         ', "\n";
   }
    
   print "\n";
   print "\n";
   print '}', "\n";
   print "\n";
   print "\n";
   print '// Python dict to SPL tuple , conversion only', "\n";
   print 'void MY_OPERATOR_SCOPE::MY_OPERATOR::fromPyDictToSPLTuple(PyObject *pyDict, ';
   print $oport->getCppTupleType();
   print ' & otuple  ';
   print $itypeparam;
   print ') {', "\n";
   print "\n";
   print '  Py_ssize_t available = PyDict_Size(pyDict); ', "\n";
   print '    ', "\n";
     if (defined $iport) {
       print 'bool setAttr = false;';
     }
   
     for (my $ai = $oport->getNumberOfAttributes() - 1; $ai >= 0; --$ai) {
       
       my $attribute = $oport->getAttributeAt($ai);
       my $name = $attribute->getName();
       my $atype = $attribute->getSPLType();
       splToPythonConversionCheck($atype);
       
       if (defined $iport) {
                print 'setAttr = false;';
       }
   print "\n";
   print '    if (available > 0) {', "\n";
   print '         // Value from the Python function', "\n";
   print '         PyObject *pyAttrValue = PyDict_GetItem(pyDict, PyTuple_GET_ITEM(pyOutNames_';
   print $oport->getIndex();
   print ', ';
   print $ai;
   print '));', "\n";
   print '         if (pyAttrValue != NULL) {', "\n";
   print '             --available;', "\n";
   print '             if (!SplpyGeneral::isNone(pyAttrValue)) {', "\n";
   print '                  streamsx::topology::pySplValueFromPyObject(', "\n";
   print '                               otuple.get_';
   print $name;
   print '(), pyAttrValue);', "\n";
       if (defined $iport) {
                print 'setAttr = true;';
       }
   print "\n";
   print '           }', "\n";
   print '        }', "\n";
   print '   }', "\n";
       if (defined $iport) {
       
       # Only copy attributes across if they match on name and type
       my $matchInputAttr = $iport->getAttributeByName($name);
       if (defined $matchInputAttr) {
          if ($matchInputAttr->getSPLType() eq $attribute->getSPLType()) {
   print "\n";
   print '    if (!setAttr) {', "\n";
   print '      // value from the input attribute', "\n";
   print '      otuple.set_';
   print $name;
   print '(ituple.get_';
   print $name;
   print '());', "\n";
   print '    }', "\n";
         }
       }
      }
   print "\n";
   print '         ', "\n";
   }
    
   print "\n";
   print '}', "\n";
    } 
   print "\n";
   }
   print "\n";
   print "\n";
   print "\n";
   SPL::CodeGen::implementationEpilogue($model);
   print "\n";
   CORE::exit $SPL::CodeGen::USER_ERROR if ($SPL::CodeGen::sawError);
}
1;
